Fixes are committed (suite green, 42 tests) and a fresh adversarial reviewer is re-running against the fixed branch. While it works, here's where triage landed.

**Fixed (all proved by a failing test first):**

| # | Defect | Criterion |
|---|---|---|
| 1 | `confirm` didn't settle — a lapsed hold confirmed cleanly; `waitlist` and `load_holds` didn't either | AC2, ADR-0003 |
| 2 | References reissued from `max(bookings)+1`, so a lapsed ref confirmed the stranger who inherited it | ADR-0001 |
| 3 | `make_book` never read `hold_minutes` — the shipped service held for 30 min, not 15 | AC1 |
| 4 | `_promote` bypassed every check in `book()`: foot passenger into a car space (`available_foot` → −1), car passenger into reserved spaces | AC3, edge cases |
| 5 | A refused second hold deleted the first, leaving the passenger with nothing | AC4 |
| 6 | `available_cars` counted confirmed only — offered spaces `book()` refused, and killed surge pricing | README |
| 7 | A `time.monotonic()` deadline on disk is meaningless after a reboot (34 hours of extra life) | AC5 |
| 8 | `hold_fee` used `round(fare * 0.1)` — a float in money, wrong for 90,000 of the first 200,000 øre | AC6, ADR-0002 |
| 9 | `save_holds` truncated its only copy; waitlist and ref counter weren't persisted | AC3+AC5 |
| 10 | `HoldDesk` and `extend_hold` — pass-through layers the brief never asked for; deleted | scope |

**Sweep for the class** turned up one hit outside the diff: `child_fare` had the same ADR-0002 float defect, fixed as minor and mechanical. The other three classes (every public method settles, every `defaults.json` key has a reader, the only file write is atomic) now come back clean.

**Records:** ADR-0004 (absolute deadlines) and ADR-0005 (waitlist per sailing and space kind) record the two decisions the fixes forced; A2 is rewritten to what Python actually documents; the README describes holds as built, with the `hold_minutes` row.

**Follow-up, not fixed:** the hold fee is computed but never charged or credited. The brief's "credited on confirmation" needs a ledger on `Booking` that doesn't exist — that's a design decision, not a fix, so I left it out rather than invent one, and kept the README from promising it. **AC6 is only half met** on this branch. Two smaller follow-ups: confirmed bookings still don't survive a restart (pre-existing — nothing persisted before this branch), and no operation looks at `Sailing.departs`, so holds can be placed on a ferry that has sailed.

I'll report the re-review and then open the PR.
