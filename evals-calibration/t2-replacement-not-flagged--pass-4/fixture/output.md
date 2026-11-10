All five reviews are done. They overlap heavily, so below are the 19 findings after merging duplicates, most severe first. Nothing in the repository is changed except one untracked file the adversarial reviewer left: `tests/test_attack_holds.py` (19 throwaway tests, 17 failing and 3 erroring). It makes a plain `python3 -m unittest` run red; the branch's own 16 tests pass.

There's no issue tracker, so this report is the only record. Step 1b didn't apply because there is no `.claude/protected-paths.txt`.

## Findings and what I'd do with each

**Fix in this change (defects)**

1. **The 15-minute default from `defaults.json` never takes effect, so holds last 30 minutes** (criterion 1). `make_book` (`ferrybook/booking.py:129`) doesn't pass `hold_minutes`, and the constructor defaults to 30 (`:31`). The tests build the book directly with 15, so they don't notice. All five reviewers found this. **Fix:** pass `settings["hold_minutes"]` in `make_book`, drop the constructor default, and build the test's book from `defaults.json` through `make_book`.

2. **A lapsed hold can still be confirmed** (criterion 2, ADR-0003). `confirm` (`:82`) never settles lapsed holds first. `test_a_lapsed_hold_cannot_be_confirmed` only passes because it calls `available_cars` first, which settles. **Fix:** settle at the top of `confirm`, and remove the workaround calls at `tests/test_holds.py:47,56`. The same gap is in `waitlist` (`:93`) and `load_holds` (`:122`).

3. **Booking references are issued again, against ADR-0001.** `_new_ref` is `max(refs)+1` (`:39`). An old ticket can then confirm or cancel another passenger's hold; the adversarial and hold-ledger reviewers both proved this. **Fix:** restore trunk's counter that only goes up, and save and load it with the holds.

4. **Promotion from the waitlist skips the capacity check** (edge case: reserved spaces are never held; criterion 4). `_promote` (`:49`) places a hold directly, so:
   - a freed foot space can go to someone waiting for a car space;
   - reserved car spaces can be held;
   - a passenger who already has a hold can get a second one.

   **Fix:** promote the first waitlisted passenger whose kind of space (car or foot) fits, through the same replace-then-check path that `book` uses.

5. **Saved deadlines rely on assumption A2, which the Python docs contradict** (criterion 5). The docs say `time.monotonic()`'s reference point is undefined. On Linux it restarts at boot, so after a reboot a saved hold would last for days. `test_holds_survive_a_restart` reuses the same fake clock, so it can't catch this. **Fix:** store wall-clock UTC deadlines. Replace A2 with a superseding entry rather than editing it, record the change with a decision record via `design:adr`, and give the restart test a clock with a different origin.

6. **The hold fee is computed with a float** (criterion 6, ADR-0002). `round(fare * 0.1)` (`ferrybook/pricing.py:26`) rounds halves to even, so a fare of 35 gives 4 rather than 3. **Fix:** `fare // 10`, plus a test with a fare that isn't a multiple of 10.

7. **The hold fee is never credited on confirmation.** The brief and the `hold_fee` docstring both promise it, but nothing calls `hold_fee`. **Fix:** implement it. What it is credited to is unclear (see #18).

8. **`available_cars` now counts only confirmed bookings** (`:105`). It disagrees with `book` and `available_foot`, which also count holds. So it can report a free space that `book` then refuses, and surge pricing ignores held spaces. **Fix:** count held spaces too, as `available_foot` does.

9. **A refused replacement loses the passenger's existing hold.** `book` (`:70`) deletes the old hold before checking for space. If the replacement raises `FullError`, the first hold is gone, and its freed space is never offered to the waitlist. **Fix:** check space first, and remove the old hold only once the new one will succeed.

10. **The waitlist isn't saved** (criteria 3 and 5). After a restart nobody is promoted. `load_holds` also overwrites existing bookings without checking. **Fix:** save the waitlist and the reference counter with the holds, and refuse to load into a book that isn't empty.

11. **`extend_hold` and `HoldDesk` (`ferrybook/holds.py`) weren't asked for.** `extend_hold` accepts any number of minutes, including negative ones, which undoes criterion 1. `HoldDesk` only forwards calls. **Fix:** delete both and `test_the_desk_places_and_confirms`.

12. **The README is now wrong.** Line 7 says "A booking is confirmed when it is made", and the configuration table has no `hold_minutes` row. **Fix:** rewrite the Bookings section, add the table row, and add one sentence on the hold fee.

13. **Free space is worked out three different ways.** `_taken` takes a list of statuses, `book` has its own inline if/else, and the two `available_*` methods differ. **Fix:** one `_free(sailing_id, vehicle)` method used everywhere. This also fixes #4 and #8.

**Fix in this change (nits)**

14. **`save_holds` doesn't write atomically.** A crash partway through a save leaves an empty or half-written file. **Fix:** write to a temporary file, then `os.replace` it into place.

15. **Choices made with no decision record:** holds are a status on a booking, they are saved as JSON, and `confirm` on an unknown or cancelled reference raises `HoldExpired`, while `get` and `cancel` raise `KeyError`. **Fix:** one ADR covering the hold model and how holds are saved, together with #5.

16. **Some tests check less than their names say.** `test_a_lapsed_hold_goes_to_the_waitlist` never checks that Bo actually got a hold. **Fix:** assert Bo's hold.

**Same kind of defect, found in the sweep**

17. **`child_fare` uses a float too** (`pricing.py:21`, `int(fare * 0.5)`). This is code from before the branch and outside its scope, but changing it to `// 2` changes no behaviour. **Fix in this change**, with a test.

**Needs your answer (the brief is unclear)**

18. Three gaps in the brief:
    - What is the fee credited to, and is it charged when the hold is placed?
    - Is the waitlist one queue per sailing, or separate queues for car and foot spaces?
    - The Behaviour paragraph releases the space only when a hold lapses, but criterion 3 also covers cancelling.

**Follow-up (outside the brief, needs design)**

19. Two things the brief doesn't cover:
    - Nothing checks whether a sailing has already departed, so holds and promotions can land on a sailing that has left. Booking a departed sailing was already possible on trunk; promotion is new.
    - A promoted passenger is never told their new reference, so their hold can lapse without them knowing.

**Rejected:** nothing. Every finding names a defect, a missed criterion, a broken decision record, a document that's now wrong, or behaviour the brief didn't ask for.

## For your fixes

Write a failing test before each defect fix. The red tests in `tests/test_attack_holds.py` already cover #1–6 and #8–11. Move the ones you want into `tests/test_holds.py` under proper names and delete the file before committing. After the fixes, re-run the adversarial lens once: the fixes are large enough to need a second round.