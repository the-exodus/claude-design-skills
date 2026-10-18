## Review cycle report

**Lenses run:** adversarial (with the repo's `ferry-attacks` lens, which extends it and matches `ferrybook/**`) and design parity. `hold-ledger` and `manifest-export` matched no changed path; platform reality wasn't triggered — the change relies on no entry in `docs/design/assumptions.md`. No lens argument was given, so none was left out.

### Findings, ranked

1. **[defect] A 00:00 sailing was listed on no day at all** — `ferrybook/schedule.py:18`. Both lenses found it independently. The branch changed `day_start <= s.departs <= day_end` to `day_start < s.departs < day_end`, tightening *both* bounds when only the upper one was wrong. AC 1's first clause — "lists a sailing departing at 00:00 on its own day" — failed: the sailing vanished instead of double-listing. **Fixed** as the half-open interval `day_start <= s.departs < day_end`. The adversarial reviewer's minute-by-minute sweep over 48 hours confirms this is the only predicate of the three with no broken instant.

2. **[defect] The branch's own test asserted only half of AC 1** — `tests/test_schedule.py:16`. `test_a_midnight_sailing_is_not_listed_on_the_day_before` passes equally when the sailing is listed nowhere, which is why the suite stayed green over the regression. **Fixed**: added `test_a_midnight_sailing_is_listed_on_its_own_day` (red before the fix: `[] != ['S3']`) and `test_the_last_sailing_before_midnight_is_listed_on_its_own_day` to pin the other end of the window.

3. **[nit] No record of the day-boundary convention** — **deferred to the follow-up below.** The brief forces half-open for `departures_on` on its own, so there was no real choice to record here; the decision only becomes one when it has to govern `arrivals_on` too, so it belongs with that fix rather than with this change.

4. **[defect, outside scope] `arrivals_on` still double-lists a midnight arrival** — `ferrybook/schedule.py:24`, left as `day_start <= s.arrives <= day_end`. **Follow-up, not fixed here**: `AGENTS.md` is explicit that a defect outside the brief is never fixed in the same change, and the brief and both criteria name `departures_on` only. Evidence: a sailing arriving at exactly `2026-06-02T00:00:00` is returned for both June 1 and June 2 (probed by both reviewers). Same one-character fix, `<= s.arrives < day_end`. Note that until it lands, the two sibling functions disagree about which day owns midnight — worth pairing the fix with the short ADR from finding 3 ("a day is the half-open interval from 00:00 up to, not including, the next 00:00"). There is no tracker, so this report is the record.

5. **[nit] Untracked attack file left the working tree red** — `tests/test_attack_midnight.py`. **Resolved**: its departure assertions were promoted into `tests/test_schedule.py` under proper names and the file deleted.

**Class sweep:** the pattern is an inclusive upper bound on a day window. The only other instance in the tree is `arrivals_on` (finding 4); the `<= 0` comparisons in `booking.py` are capacity checks, not intervals.

**State:** `python3 -m unittest` → 11 tests, OK. Committed as `077374a` on `fix-midnight-departures`. Nothing pushed. Ready for the PR — mention finding 4 in its description so the maintainers can schedule it.
