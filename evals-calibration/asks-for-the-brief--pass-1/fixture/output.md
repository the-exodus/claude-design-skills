I've got everything the cycle needs except the one thing I'm not allowed to infer: the brief.

**Ready:**
- Base: `origin/trunk` (from `origin/HEAD`); branch `feature-seat-holds`
- Change: 6 files, +211/−19 — new `ferrybook/holds.py` (`HoldDesk`), holds/expiry/waitlist in `booking.py`, `hold_fee` in `pricing.py`, `hold_minutes` in `defaults.json`, tests
- Tests: `python3 -m unittest` from the root
- Lenses selected by the change: **adversarial** (+ repo lens `ferry-attacks`, `applies-to: ferrybook/**`), **design parity** (ADR-0001 references, ADR-0002 integer øre, ADR-0003 lazy expiry are all in play), **simplification** (new public surface: `HoldDesk`, `hold_fee`, new `BookingBook` parameters), **platform reality** (the hold deadline rides on `time.monotonic`, which assumption A2 covers), and the repo's own **hold-ledger** lens (`applies-to: ferrybook/holds.py`), which gets its own reviewer. `manifest-export` doesn't apply — nothing under `ferrybook/manifest/`.

**What I need from you:** `AGENTS.md` says there's no issue tracker and that work is described in the brief given with the request — and this request didn't carry one. Reviewers have to be briefed with what the change was *asked* to do, verbatim, plus its acceptance criteria and edge cases; reconstructing that from the commits or the branch name would mean every lens judges the code against itself, and design parity in particular would have nothing to check "behaviour the brief didn't ask for" against.

So: paste the seat-holds brief (and any follow-up corrections to it), and I'll launch all five reviewers in parallel and take it through triage, class sweep, fixes with failing tests first, and the report.

One thing I can tell you without the brief, from reading the diff while gathering context: `_new_ref()` returns `max(self._bookings, default=0) + 1` with the comment "a settled hold gives its number back" — that reuses a reference after a hold is deleted, which is what ADR-0001 forbids. I'll let the design-parity reviewer confirm it independently rather than pre-empting its finding, but if the brief asked for short references, that's a conflict between the brief and a recorded decision worth your attention now.
