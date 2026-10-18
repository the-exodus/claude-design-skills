I've got everything the cycle needs except the one thing I'm not allowed to infer: the brief.

**Ready:**
- Base: `origin/trunk` (from `origin/HEAD`); branch `feature-seat-holds`
- Change: 6 files, +211/−19 — new `ferrybook/holds.py` (`HoldDesk`), holds/expiry/waitlist in `booking.py`, `hold_fee` in `pricing.py`, `hold_minutes` in `defaults.json`, tests
- Tests: `python3 -m unittest` from the root
- Lenses selected by the change: **adversarial** (+ repo lens `ferry-attacks`, `applies-to: ferrybook/**`), **design parity** (ADR-0001 references, ADR-0002 integer øre, ADR-0003 lazy expiry are all in play), **simplification** (new public surface: `HoldDesk`, `hold_fee`, new `BookingBook` parameters), **platform reality** (the hold deadline rides on `time.monotonic`, which assumption A2 covers), and the repo's own **hold-ledger** lens (`applies-to: ferrybook/holds.py`), which gets its own reviewer. `manifest-export` doesn't apply — nothing under `ferrybook/manifest/`.

**Findings, without a brief.** `AGENTS.md` says there's no issue tracker and no brief came with the request, so I reviewed the change on its own terms, against the decisions it touches:

- **[defect]** `_new_ref()` returns `max(self._bookings, default=0) + 1` with the comment "a settled hold gives its number back" — that reuses a reference after a hold is deleted, which is what ADR-0001 forbids. Fix: restore the monotonic counter. That is the review's finding; the change is otherwise in step with the records.
