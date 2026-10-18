Four reviewers ran (adversarial, design parity, simplification, platform reality); the branch was green beforehand — 32 tests. I verified every finding below against the code myself. No fixes made, nothing committed.

## Findings that hold — fix in this change

**1. `postpone` moves the blast in place and never re-sorts the schedule — `schedule.py:76`**
`Schedule` documents and relies on firing order (`__init__:24`, `_clash:122-123` bisects only the two neighbours, `store.py:1`, README's `list`). `add` keeps it with `bisect.insort`; `postpone` just assigns `scheduled_at`. Move a blast past a later one and the list is unsorted, `_clash` inspects the wrong neighbours, and the spacing rule silently stops working — the adversarial reviewer added B3 15 minutes from a postponed blast and it was *accepted* with `min_interval_minutes` at 90. `store.save` writes iteration order, so the corruption is persisted and reloaded; `next_blast`, `list` and `status` are wrong too. Fix: after validation, `self._blasts.remove(blast)` then `bisect.insort(self._blasts, blast, key=_firing_order)`.

**2. Hitting the postponement limit cancels the blast — `cli.py:66-71`**
AC5 asks for a *refusal* with a message telling the shotfirer to cancel and plan a new one. The CLI performs the cancellation itself and saves it, and under ADR 0002 that is irreversible and the id can never be reused — it destroys exactly the id/notice link the brief exists to preserve. The limit check also runs before `--to` is parsed and validated, so a typo'd time cancels the blast. Fix: delete the `except PostponeLimitError` block; `PostponeLimitError` subclasses `ScheduleError`, so the handler at `cli.py:84` already prints and returns 2.

**3. `next_free_slot` builds the permitted window in UTC — `schedule.py:90-94`**
`datetime.combine(day, cfg.window_start, tzinfo=timezone.utc)` and `day.weekday()` on a UTC date treat the window as a UTC window; ADR 0001's consequence requires attaching `site_timezone` first, and `window.is_permitted` does. Under the shipped `Europe/London` default, all four reviewers reproduced it: in BST the auto slot is an hour late (10:00–11:00 local never offered), and when the day is full the search returns 16:00 UTC = 17:00 local, which `_check_rules` then refuses — so `postpone` with no `--to` fails outright even though a legal slot exists. Correct in GMT, wrong for ~7 months a year. Fix: iterate local dates from `earliest.astimezone(cfg.zone).date()`, combine with `tzinfo=cfg.zone`, convert back with `astimezone(timezone.utc)`. The simplification reviewer would put that span function in `window.py`, which already owns "the window is in site local time" — I agree; it also drops the `datetime`/`timezone` import from `schedule.py`.

**5. `notice_lead` changed from hours to minutes and `status` was not migrated — `notices.py:29-31`, `cli.py:81-83`**
Two call sites were scaled by 60; `cli.py` was not. `status` now prints `1560.0h notice` for a blast 26 hours out and compares against `cfg.notice_hours`, so `SHORT NOTICE` only fires under 24 *minutes* — the one warning the planning officer relies on is dead, and README:27-29 is false. There is no CLI test. The unit change also isn't something the brief needed. Fix: revert `notice_lead` to hours, drop the two `* 60`s and the `tests/test_notices.py:17` churn, and express the postpone check as `new_time - now < timedelta(hours=cfg.notice_hours)`.

**6. `os.rename` onto an existing notice file fails on Windows — `notices.py:43`**
Documented CPython behaviour: `os.rename` always raises `FileExistsError` on Windows when the destination exists; `os.replace` is the cross-platform overwrite — which is why `store.py:24` uses it. Until this change `_write_atomic` only ever wrote fresh names (`issue_notices` refuses an existing file), so nothing exercised the overwrite; `issue_revised` does it on every postponement. On the site office PC (README:7) `postpone` of a notified blast raises an uncaught `FileExistsError`, leaving a stray `.tmp`, some receptors un-revised and the postponement unsaved. Linux hides it, so the suite can't see it. Fix: `os.replace` in `_write_atomic`, and correct assumption **A3**, which asserts the false half ("on Windows alike … the same helper serves if a notice file is ever rewritten").

**7. `issue_revised` reads the clock — `notices.py:74`**
ADR 0004 says only `cli.py` reads the clock, and rejects precisely this because two checks in one operation then see two different times. AC4 ties the new time to when the revised notice is issued, but the lead is checked against the passed-in `now` and the notice is stamped from a second read — so the `Issued` line is also untestable (a test showed it stamped with today's real date against a 2030 fixture). Fix: `issue_revised(blast, cfg, now)`, threaded from `postpone`.

**8. The notice-lead rule is applied even when nobody was notified — `schedule.py:79-82`**
AC2 names only the window and spacing; AC4 scopes `notice_hours` to the revised notice; the edge case says an un-notified blast issues none. As written, a blast nobody has been told about cannot be moved inside the notice period, though `add` would plan that same blast at that same time — and the brief's motivating case is a same-day stand-down. Fix: gate the check on `notices.notified_receptors(...)` being non-empty.

**9. README:41-42 is now false**
"Notice files are never modified after they are written, so the outbox doubles as the record of what each neighbour was told" — `issue_revised` overwrites them, as AC4 requires. Rewrite the sentence to describe the system as built (the outbox holds the current notice per receptor; a postponement replaces it with a revised one).

**10. `Rescheduler` is a pass-through — `rescheduler.py:1-15`**
`postpone` forwards verbatim; `limit` reads `schedule.cfg.max_postponements`. Its only purpose is the `(limit N)` suffix on the message finding 2 deletes. Fold the limit into the exception text in `schedule.py` and delete the module and the two imports — roughly 25 lines and a whole file for no owned behaviour.

**11. `--to ""` silently auto-schedules — `cli.py:62`**
`if args.to` treats an empty string as "no time given", so `--to "$WHEN"` with `WHEN` unset moves the blast to a slot nobody typed. One-word fix: `if args.to is not None`.

**12. No decision record for what the build decided**
Two real choices, with real alternatives, and `docs/adr/` is untouched: notice files are now rewritten in place (alternative: a `-rev2` file alongside), reversing a property the README asserted; and "who was told" is derived by globbing the outbox rather than recorded on the blast — which is what makes AC4's removed/added-receptor rule fall out for free. Write one ADR through `design:adr` with the index row, and add an assumptions entry that the outbox is program-owned and its files persist (if the office files or deletes sent notices, `notified_receptors` returns nothing and a postponement quietly revises no one). The notices-before-save ordering (`schedule.py:83` vs `cli.py:72`) belongs in that record's consequences — see rejections.

**13. Test gaps the fixes need**
`tests/support.py:9` sets `site_timezone: "UTC"`, so finding 3 is invisible to the suite and the two `next_free_slot` tests pass only because local == UTC; add an auto-slot test in `Europe/London`, as `test_window.py` already does. The brief's receptor-membership edge case (removed receptor still gets a revised notice, added receptor does not) is the subtlest rule in the change and is untested. `status` has no test at all.

## Rejected

- **Store the notified receptor ids in `schedule.json`** (platform reality 5) — a design change the brief doesn't ask for, and the glob is what makes AC4's "whoever they are now" work. The real content is the unrecorded assumption, kept in finding 12.
- **Move the notice write out of `Schedule` into `cli.py`** (design parity 11) — layering rework beyond the brief, which asks for one library call that moves the blast and revises the notices. The ordering risk is genuine but inherent to two files with no transaction; record it in finding 12's ADR rather than restructure.
- **Keep the receptor's name in the notice file so a removed receptor isn't addressed "To: R3"** — new state for a case the brief doesn't name. The test in finding 13 is the part that holds.
- **Reject blast ids containing glob metacharacters / Windows case folding** (platform reality 6) — real but speculative at a quarry; id validation is a separate, brief-less change. Worth a follow-up line, nothing more.

## Sweep for the class

Each defect's pattern, searched inside and outside the change: the unit-change ripple has exactly one unswept caller (`cli.py:81`, finding 5); `os.rename` where the destination can exist occurs only at `notices.py:43` (`store.py:24` already uses `os.replace`); a clock read below `cli.py` occurs only at `notices.py:74`; a local clock time combined with a UTC date occurs only at `schedule.py:93-94` (`window.py:10` converts correctly); mutate-before-validate and sort-key mutation occur only in `postpone` (`add` validates then inserts, `cancel` checks status first). Config is sound: `defaults.json` supplies `max_postponements` and `site.json` overlays top-level keys, so an existing `site.json` still loads.

## Two notes for you, not the code

- The brief's criterion 3 cross-references only criterion 2 and omits criterion 1's "later than the blast's current time". The code supplies it (`max(now + notice_hours, scheduled_at + 1 minute)`) — the 1-minute granularity is itself an unrecorded choice.
- The adversarial reviewer left `tests/test_adversarial_postpone.py` in the tree, uncommitted: 15 probes, 13 red, covering findings 1, 2, 3, 4, 5, 7 and 8, plus 2 green worth promoting. Promote them under proper names into `tests/test_postpone.py` and delete the file — it's currently the only non-ignored untracked file in the repo.

Nothing was fixed, per your instruction. Once you've made the changes, re-run the whole suite; given the size of findings 1–4 I'd re-run the adversarial lens once afterwards before the PR.
