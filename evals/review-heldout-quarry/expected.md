# Answer key: review-heldout-quarry

Project: `blastplan`, a blast scheduler for an invented quarry (Cold Ash).
Branch under review: `feature-postpone-blast` (one commit on top of `main`).
Brief: `brief.md`. Line numbers are on the branch.

10 planted defects (D1–D10), 3 traps (T1–T3).

## Defects

### D1 (kind 1: interruption, a rejected call leaves state changed)
- **Where:** `blastplan/schedule.py:76-78` (`Schedule.postpone`)
- **What is wrong:** `postpone` assigns `blast.scheduled_at = new_time` and
  increments `blast.postponements` *before* `_check_rules` and the notice-lead
  check. When either check raises, the blast is left at the refused time with
  its counter used up. AC2 and AC4 hold only for the error message, not for the
  schedule's state, and repeated refused attempts spend the AC5 allowance.
- **Failing scenario:** test settings; B1 at 2030-06-17 10:00 UTC, B2 at
  2030-06-17 13:00 UTC; `postpone("B1", 2030-06-17 12:00 UTC, now=2030-06-14 09:00 UTC)`
  raises "less than 90 minutes from blast B2", but afterwards
  `get("B1").scheduled_at == 12:00` and `postponements == 1`. A second refused
  attempt makes `postponements == 2` and the next valid postpone raises
  `PostponeLimitError` though the blast was never moved. A retry is also checked
  for "later than current time" against the refused time.
- **Smallest fix:** run `_check_rules(new_time, blast.id)` and the notice check
  before mutating; assign the time and increment the counter only after both pass.

### D2 (kind 1: ordering; the schedule's firing-order invariant is broken)
- **Where:** `blastplan/schedule.py:76` (in-place `blast.scheduled_at = new_time`)
- **What is wrong:** `Schedule` keeps `_blasts` in firing order (`add` uses
  `bisect.insort`; `__init__` and `store.load` trust the saved order), and
  `_clash` looks only at the bisected neighbours, `next_blast` returns the first
  match. `postpone` changes the time in place without moving the blast, so
  postponing a blast past another leaves the list out of order; later spacing
  checks miss clashes (AC2 for any later add/postpone), `next_blast` and `list`
  are wrong, and `store.save` persists the wrong order, so the damage survives
  across CLI runs.
- **Failing scenario:** test settings (90 min). Add A 2030-06-17 10:00 UTC, B
  12:00 UTC. `postpone("A", 14:00, now=2030-06-14 09:00)` succeeds; order is now
  `[A(14:00), B(12:00)]`. `next_blast(2030-06-17 09:00)` returns A (should be B).
  `add(C at 14:30)` is accepted, 30 minutes after A.
- **Smallest fix:** after a successful move, remove the blast and
  `bisect.insort(self._blasts, blast, key=_firing_order)` (or re-sort).

### D3 (kind 2: holds under test settings, not under shipped defaults)
- **Where:** `blastplan/schedule.py:93-94` (`next_free_slot`, also `earliest.date()` at :90)
- **What is wrong:** the window bounds are built with `tzinfo=timezone.utc`
  instead of the site zone, contradicting ADR 0001 ("must attach
  `site_timezone` and convert to UTC"). Tests use `site_timezone: "UTC"`, so
  they pass; with the shipped `defaults.json` (`Europe/London`) the search
  window is an hour late during BST, so AC3 fails.
- **Failing scenario:** shipped defaults. A planned at 2030-06-18 09:00 UTC
  (10:00 BST). `postpone("A", None, now=2030-06-17 15:30 UTC)`: earliest is
  2030-06-18 15:30 UTC, the search returns 15:30 UTC (16:30 BST), and the
  window check raises "outside the permitted window". Correct: 2030-06-19
  09:00 UTC (10:00 BST). Also: A at 2030-06-17 09:00 UTC, now 2030-06-14 08:30
  UTC: returns 10:00 UTC (11:00 BST) instead of 09:01 UTC (10:01 BST), not the
  earliest slot.
- **Smallest fix:** `datetime.combine(day, start, tzinfo=self.cfg.zone).astimezone(timezone.utc)`
  (same for end), iterating over site-local dates (`earliest.astimezone(cfg.zone).date()`).

### D4 (kind 3: contract changed, an old caller still relies on the old meaning)
- **Where:** `blastplan/notices.py:29-31` (`notice_lead` now returns minutes);
  stale caller `blastplan/cli.py:81-83` (`status`).
- **What is wrong:** `notice_lead(blast, issued_at)` changed from float hours
  to int minutes with the same signature. `issue_notices` and `postpone` were
  updated (`* 60`), but `cli status` still compares with `cfg.notice_hours` and
  prints `h`. The README's `status` description is now false in practice.
- **Failing scenario:** a planned blast 2 hours away: `status` prints
  `120.0h notice` and no `SHORT NOTICE` flag (120 >= 24). Any blast at least 24
  minutes away is never flagged; a blast 30 h away shows `1800.0h`.
- **Smallest fix:** keep `notice_lead` in hours and compare with
  `cfg.notice_hours` in `postpone`, or add a separate minutes function; or
  update `cli status` (`lead / 60`, compare with `notice_hours * 60`).

### D5 (kind 4: contradicts ADR 0004, the clock is passed in)
- **Where:** `blastplan/notices.py:74` (`issue_revised`: `issued = datetime.now(timezone.utc)`)
- **What is wrong:** library code reads the clock, the mechanism ADR 0004
  rejected ("Only `cli.py` reads the clock"). `postpone` checks AC4 against the
  passed `now` but the revised notice is stamped with a different, real time,
  so the two checks in one operation see two different times, and tests cannot
  control the "Issued" line.
- **Scenario:** `postpone(..., now=2030-06-14 09:00)` writes a revised notice
  saying "Issued 2026-…" (the wall clock), not 2030-06-14 09:00.
- **Smallest fix:** `issue_revised(blast, cfg, now)` and pass `now` from `postpone`.

### D6 (kind 5: user-facing doc made false)
- **Where:** `README.md:41-42` ("Notice files are never modified after they are
  written, so the outbox doubles as the record of what each neighbour was told.")
- **What is wrong:** the branch overwrites notice files with revised notices
  (AC4), so the sentence is false, and the original notice text is lost from
  the "record". The branch edited the README (postpone section, config row) but
  left this sentence.
- **Smallest fix:** reword: notices are rewritten when a blast is postponed;
  the outbox shows the latest notice each neighbour was sent.

### D7 (kind 6: unrecorded decision between real alternatives)
- **Where:** `blastplan/notices.py:34-37` (`notified_receptors`), used at :76.
- **What is wrong:** to know who received the original notice, the branch
  chose to infer it from which notice files are present in the outbox, rather
  than recording the notified receptor ids on the blast (or in the schedule
  file). That makes the outbox directory part of the system's state: if the
  office moves or deletes sent notices (or `outbox` is changed in site.json),
  postponements silently send no revised notice. No ADR or note records this,
  and nothing warns the office not to tidy the outbox.
- **Smallest fix:** add an ADR (or README/assumptions note) recording that the
  outbox files are the record of who was notified and must not be moved, with
  the alternative considered; or store the notified ids on `Blast`.

### D8 (kind 7: behaviour the brief did not ask for)
- **Where:** `blastplan/cli.py:66-71` (`except PostponeLimitError` branch)
- **What is wrong:** when the postponement limit is reached, the CLI cancels
  the blast and saves. AC5 asks only that postponing be refused with a message
  telling the shotfirer to cancel and re-plan. Auto-cancelling is irreversible
  (ADR 0002: cancelled blasts stay cancelled, ids are never reused) and happens
  on what the user meant as a postpone.
- **Scenario:** blast postponed twice (default `max_postponements: 2`);
  `blastplan postpone B14 --to ...` cancels B14.
- **Smallest fix:** print the error and return 2 without calling `cancel`/`save`.

### D9 (kind 8: needless pass-through layer)
- **Where:** `blastplan/rescheduler.py:4-15` (class `Rescheduler`), used at `blastplan/cli.py:63-65`.
- **What is wrong:** `Rescheduler.postpone` only forwards to
  `Schedule.postpone` with the same arguments, and `limit` only reads
  `schedule.cfg.max_postponements`. It adds a module and a name with no
  behaviour of its own.
- **Smallest fix:** delete `rescheduler.py`; the CLI calls
  `schedule.postpone(...)` and reads `cfg.max_postponements`.

### D10 (kind 9: external assumption wrong per the Python docs)
- **Where:** `blastplan/notices.py:87` (`issue_revised` calls `_write_atomic`
  on an existing notice), relying on `blastplan/notices.py:43`
  (`os.rename(tmp, path)`) and assumption A3 (`docs/design/assumptions.md:21-28`).
- **What is wrong:** A3 claims a rename onto an existing name replaces it on
  Linux and Windows alike. The Python docs for `os.rename` say: "On Windows,
  if dst exists a FileExistsError is always raised"; `os.replace` is the
  cross-platform replacing rename. Base code only ever renamed onto new names;
  the branch is the first to rename over an existing file. README says the tool
  runs on the site office PC (Windows).
- **Scenario:** on Windows, `notify B14` then `postpone B14 --to ...` raises
  `FileExistsError` from `os.rename` (uncaught by the CLI, which catches only
  ScheduleError/NoticeError), after `postpone` already moved the blast in memory.
- **Smallest fix:** use `os.replace(tmp, path)` in `_write_atomic`, and correct A3.

## Traps (correct as written)

### T1: inclusive window end in the slot search
- **Where:** `blastplan/schedule.py:96` (`while candidate <= end:`)
- **Why it looks wrong:** a half-open `[start, end)` window is the usual
  convention; `<= end` lets a slot land exactly on 16:00 and reads like an
  off-by-one.
- **Why it is correct:** ADR 0003: "A blast at exactly the window's start or end
  time is permitted. Every check or search against the window treats `end` as
  the last permitted firing time, not as the first forbidden one." and
  "Comparisons against `window.end` use `<=`." (The UTC construction of `end`
  on line 94 is D3; the `<=` is not a defect.)

### T2: postpone does not re-run the vibration check
- **Where:** `blastplan/schedule.py:56-84` (`postpone` never calls
  `vibration.within_limit`, unlike `add` at :41)
- **Why it looks wrong:** `postpone` re-validates window and spacing but skips
  the PPV limit, which looks like a missing validation.
- **Why it is correct:** brief AC6: "Postponing does not repeat the vibration
  check: the charge and distance do not change, and the prediction does not
  depend on the time of day."

### T3: revised notices ignore the current receptor list
- **Where:** `blastplan/notices.py:75-80` (`issue_revised` takes recipients from
  `notified_receptors`, uses `cfg.receptors` only for names, falling back to the id)
- **Why it looks wrong:** it looks like stale data: a receptor added to the
  configuration gets no revised notice, and one removed still gets one.
- **Why it is correct:** brief edge case: "a receptor removed from the
  configuration since the original notice still gets one, and a receptor added
  since does not (they were never told of the blast and will get notices for
  future blasts)." (Whether inferring recipients from outbox files is a good,
  recorded choice is D7; flagging only "ignores current receptors" is a trap hit.)

## Distinctive words for graders

- D1: `postpone`, `scheduled_at = new_time`, `postponements += 1`, `_check_rules`, before/after validation, mutate, rollback, refused/rejected leaves, state
- D2: `bisect`, `insort`, firing order, sorted/unsorted, `_clash`, neighbours, `next_blast`, re-sort, order
- D3: `timezone.utc`, `next_free_slot`, `datetime.combine`, `Europe/London`, BST, `site_timezone`, `cfg.zone`, defaults.json, 16:30
- D4: `notice_lead`, minutes, hours, `status`, `SHORT NOTICE`, `cli.py`, units, `* 60`
- D5: `datetime.now`, ADR 0004, clock, `issue_revised`, `now` parameter, `issued`
- D6: README, "never modified", outbox, record, overwrit/replac, revised notice
- D7: `notified_receptors`, `glob`, outbox as record/state, archive/move/delete notice files, ADR/undocumented/decision, store notified ids
- D8: `PostponeLimitError`, `cancel`, auto-cancel, cancels the blast, not asked/brief, AC5
- D9: `Rescheduler`, `rescheduler.py`, pass-through, forwards, wrapper, `limit`
- D10: `os.rename`, `os.replace`, Windows, `FileExistsError`, assumption A3, `_write_atomic`
- T1 (should not be flagged as a defect): `<= end`, inclusive, ADR 0003, 16:00, off-by-one, half-open
- T2 (should not be flagged): vibration, `within_limit`, PPV, not re-checked, AC6
- T3 (should not be flagged): `cfg.receptors`, receptor added/removed, current receptors, names.get
