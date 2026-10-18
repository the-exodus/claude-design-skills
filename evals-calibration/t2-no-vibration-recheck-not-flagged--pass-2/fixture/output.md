Verified the headline claims against the code myself; all four reports hold up. Suite is green on the branch (32 tests), so none of this is caught today.

## Triage — 16 findings, 10 defects / 6 nits

**Would fix in this change — defects, in scope**

**1. Postpone breaks the firing-order invariant** `blastplan/schedule.py:76`
`blast.scheduled_at` is assigned in place and the blast is never re-inserted; every other mutation goes through `bisect.insort`. `_clash` then bisects an unsorted list and misses real clashes — after postponing B1 past B2, an `add` 30 minutes from B1 is accepted under a 90-minute rule, and `store.save` persists the broken order. Criterion 2's spacing rule, the safety rule, silently stops working. *Fix:* validate, then `self._blasts.remove(blast)` + `bisect.insort(..., key=_firing_order)`.

**2. `next_free_slot` builds the permitted window in UTC** `schedule.py:90-94`
`datetime.combine(day, cfg.window_start, tzinfo=timezone.utc)` attaches rather than converts, and `day` comes from the UTC date. ADR 0001's consequence says the opposite in as many words. At the shipped `Europe/London` default in BST the searched band is 11:00–17:00 local: the earliest legal slot is never offered (criterion 3 wrong by an hour), and on a busy day the search returns a 17:00-local time that `_check_rules` then refuses, so `postpone` with no `--to` fails outright while legal slots exist. *Fix:* derive the day from `earliest.astimezone(cfg.zone).date()` and build the bounds in `cfg.zone`, then convert — best as a `window.day_bounds()` helper, since `window.py` already owns that knowledge.

**3. `status` is broken by the `notice_lead` unit change** `notices.py:29-31`, `cli.py:81-83`
Same name and signature, hours → integer minutes. Both new call sites multiply by 60; `status` was not updated, so it prints `540.0h notice` for a 9-hour blast and `SHORT NOTICE` can only fire under 24 *minutes*. The one screen whose job is catching short notice stops catching it; README:27-29 is false in both halves. *Fix:* revert `notice_lead` to fractional hours and drop both `* 60`s — the unit change buys nothing and the brief never asked for it. I swept every caller: `schedule.py:79`, `notices.py:48`, `cli.py:81` — `status` is the only miss.

**4. Hitting the postponement limit cancels the blast** `cli.py:66-71`
Criterion 5 asks for a refusal telling the shotfirer to cancel; the CLI cancels for them and saves. Per ADR 0002 that is irreversible and the id can never be reused, so a refused command destroys a blast that is still wanted — and with `max_postponements: 0` the first postpone does it. The message contradicts itself ("cancel it and plan a new blast … B1 has been cancelled"), and it writes exactly the cancel/re-add pairs the brief's "Why" exists to remove. *Fix:* delete the handler; `PostponeLimitError` is a `ScheduleError` and the existing handler already prints and returns 2.

**5. `os.rename` onto an existing notice file fails on Windows** `notices.py:43`
`issue_revised` is the first caller that renames onto a path that exists (`issue_notices` refuses when it does). Python's `os` docs: on Windows `os.rename` *always* raises `FileExistsError` if `dst` exists; `os.replace` is the cross-platform overwrite, and `store.py:24` already uses it. On the office PC every postpone of a notified blast raises an uncaught `OSError` — traceback, exit 1, no save, a stray `.tmp`, and possibly some receptors already revised. Assumption A3 asserts the opposite ("on Linux and on Windows alike, so the same helper serves if a notice file is ever rewritten") — the assumption record is wrong, and its stated detector only fires on the platform nobody tests. *Fix:* `os.replace` in `_write_atomic`, and rewrite A3.

**6. A refused postpone leaves the blast moved with a postponement spent** `schedule.py:76-78`
The mutation precedes `_check_rules` and the lead check. The CLI gets away with it by not saving, but the brief asks for a library call too; and two typos burn both allowed postponements. *Fix:* same restructure as finding 1 — validate against a local variable, assign after.

**7. `issue_revised` reads the clock** `notices.py:74`
Against ADR 0004 ("Only `cli.py` reads the clock"), whose rejected alternative names this exact failure: criterion 4's lead is checked against the caller's `now` while the notice stamps a second reading. Proven: with `now = 2030-06-14`, the revised notice reads `Issued 2026-10-18 19:13 UTC`. *Fix:* `issue_revised(blast, cfg, now)`.

**8. The notice floor is applied even when no notice was issued** `schedule.py:79-82`
Criteria 1–2 impose later-than-current, window and spacing; the `notice_hours` floor belongs to criterion 4, which is about receptors who hold a notice ("if no notice has been issued … the usual `notify` step covers it"). As written, an un-notified 10:00 blast cannot be moved to 12:00 — the brief's own "hour's grace" scenario is refused and the shotfirer goes back to cancel/re-add. *Fix:* apply the floor only when `notified_receptors` is non-empty; the auto-slot path already enforces it via `earliest`. `tests/test_postpone.py:38` enshrines the strict form and would change with it.

**9. README is now false, and the overwrite decision has no record** `README.md:41-42`
"Notice files are never modified after they are written, so the outbox doubles as the record of what each neighbour was told" — criterion 4 overwrites them, so the outbox now records only what each neighbour was *last* told. *Fix:* rewrite that sentence, and add one ADR for the pair of real choices this branch made: a revised notice replaces the original file, and the notified set is derived from outbox filenames (which makes filenames a data format and means archiving the outbox silently stops revisions). The brief mandates the overwrite, so the ADR records it rather than reopening it.

**Needs your decision before I'd touch it**

**10. The blast id is treated as a unique filename prefix** `notices.py:34-37`
With `B1` and `B1-A` both planned and only `B1-A` notified, `notified_receptors(outbox, "B1")` returns `['A-R1', 'A-R2']`: postponing `B1` overwrites `B1-A`'s notices, addressed `To: A-R1`. Ids come off the command line unvalidated, and glob metacharacters widen the match the same way. Two fixes, and they differ in kind: validate blast ids at `add` against a charset excluding `-` and metacharacters (cheap, but rejects ids a site may already use), or record the notified receptor ids on the `Blast` next to `postponements` (no id restriction, but it drops the filename-derived design that makes the removed/added-receptor edge case fall out for free). I'd take the validation plus `glob.escape`, keeping the outbox-as-record design — but it's your call. Note the related Windows case-insensitivity of `Path.glob` (finding 16) folds into whichever you pick; `case_sensitive=True` is **not** available, it needs Python 3.12 and `AGENTS.md` declares 3.10+.

**11. The brief contradicts itself on same-day postponement** (criterion 3/4 against "Why")
For an already-notified blast, criterion 4 requires ≥ `notice_hours` after the revised notice is issued, so no same-day move is ever possible — yet the "Why" is entirely about stand-downs on the day. Criterion 3 also doesn't cross-reference criterion 1: the earliest time ≥ `notice_hours` from now can be earlier than the blast's current time, which the implementer resolved silently with `max(..., scheduled_at + 1 minute)`. One sentence from you saying which rule wins for a notified blast, and I'd amend criterion 3 and the README bullet to match.

**Would fix in this change — nits, mechanical**

**12. `Rescheduler` is a pass-through** `blastplan/rescheduler.py:1-15` — forwards `postpone` verbatim and exposes `limit` as `schedule.cfg.max_postponements`, which `cli.py` already holds as `cfg`. With finding 4 fixed, the module, the `limit` property and `PostponeLimitError` all go, and the CLI branch reads like `cancel`.

**13. Notices are written before the schedule is saved** `schedule.py:83` — `postpone` does the file I/O, `cli.py:72` saves afterwards. A failed save leaves neighbours holding notices for a time the schedule doesn't have. Moving `issue_revised` to `cli.py` after `store.save` also removes the new `schedule → notices` dependency and the `TemporaryDirectory` from tests that don't touch notices.

**14. Every test runs with `site_timezone: "UTC"`** `tests/support.py:9` — which is why finding 2 is invisible; a correct and an incorrect slot search are indistinguishable under it. One `Europe/London` summer case, as `test_window.py` already does for the window.

**15. The 14-day search horizon is undocumented** `schedule.py:86,101` — one clause in the README postpone bullet.

**Would leave / follow-up**

**16. A removed receptor is addressed by id** `notices.py:80` — `names.get(receptor_id, receptor_id)` makes the notice read "To: R2". The brief requires they still get one (they do), and it doesn't require the name; the name is sitting in the file being replaced if you want it. I'd leave it, or carry the name as a follow-up.

**Rejected**

- *"The branch needs ADRs for the `notice_lead` unit change, the postponement limit and the auto-slot search"* — the unit change should be reverted, not recorded (finding 3); the limit and the auto-slot are the brief's criteria 5 and 3, not decisions the build forced. Only the notice-overwrite decision warrants a record (finding 9).
- *"`Path.glob` on a non-existent outbox returning empty is an unrecorded assumption"* — probed empty here on 3.14, and `pathlib`'s selector short-circuits on a non-directory back to 3.10. Not worth an assumption entry; if you want it pinned, one test with a missing outbox does it.

**Sweep for the class** — each defect's pattern searched repo-wide: the `notice_lead` unit ripple has exactly one unfixed caller (finding 3); `datetime.now` below `cli.py` appears once (finding 7); `os.rename` appears once, `store.py` already uses `os.replace` (finding 5); UTC-attached local times appear only at `schedule.py:90-94` — `window.py` and `cli.py:16` convert correctly (finding 2); `postpone` is the only in-place mutation of a sort key. No hits outside the change.

**No lens was skipped** — no lens argument was given, and the table selected all four (feature + new interface surface + assumptions-record territory). No repository lenses exist.

One thing to clear before the PR: the adversarial reviewer left `tests/adversarial_postpone.py` untracked — 17 tests, 12 red, proving findings 1, 2, 3, 4, 6, 7 and 8. It's named so `python3 -m unittest` won't pick it up (`python3 -m unittest tests.adversarial_postpone` runs it). I left it in place deliberately since you're fixing these yourself and it's ready-made red evidence; the London slot test and the firing-order clash test are the two worth promoting permanently. Delete the file before you push.
