The review cycle is complete. Push is blocked — the sandbox refuses outbound to `git.ferrybook.example`, so I committed the fixes locally but could not open the PR.

## What ran

Six reviewers, none sharing this conversation: **adversarial** (with the repo's own `ferry-attacks` list), **design parity**, **simplification** (the change adds interface surface), **platform reality** (it leans on the assumptions record), and the repo's **hold-ledger** lens — then one fresh adversarial re-run over the fixes, which found a second round. `manifest-export` wasn't selected; nothing under `ferrybook/manifest/**` changed. No lens argument was given, so none was left out.

## Fixed — defects (each with a failing test first; suite 16 → 39 tests, green)

1. **`confirm` never settled, so a lapsed hold confirmed happily** — AC2 failed outright, and ADR-0003 says every public operation settles first. The two shipped tests only passed because they called `available_cars` first to force the sweep; those priming lines are gone.
2. **References were reused** — `max(bookings)+1` handed a cancelled or lapsed hold's number to the next passenger, reversing ADR-0001 in the ADR's own words ("even when that would keep references short"). Ada's printed ticket resolved to Bo's booking. Monotonic counter restored and persisted.
3. **`hold_minutes` never reached production** — `make_book` didn't pass it, so every real hold lasted the constructor's 30 minutes, not the shipped 15. AC1 was met only in tests.
4. **Three different answers to "is a held space taken?"** — `book` said yes, `available_foot` yes, `available_cars` no. Surge pricing never fired on held car spaces, and the desk was shown spaces that `book` refused. One rule now (`_free`), recorded as **ADR-0004**.
5. **Waitlist promotion bypassed every check** — no capacity test, no reserved-space test, wrong deck, and it could hand a passenger a second space. A promoted passenger could be put straight into an emergency-vehicle space.
6. **A refused booking destroyed the passenger's existing hold** — the earlier hold was deleted before the capacity check.
7. **Holds did not survive a restart** — `time.monotonic()`'s reference point is undefined (assumption A2 was false as written); after a reboot a restored hold wedged its space for roughly the previous uptime. Deadlines are now wall-clock instants, recorded as **ADR-0005**, and A2 is rewritten.
8. **Restart lost paid bookings and resold their spaces**, dropped the waitlist, overwrote live references, and crashed on a sailing that had left the timetable. The file now carries bookings, waitlist and counter, is written atomically, validates before mutating, and settles on load.
9. **Float money** — `round(fare * 0.1)` rounded *against* the passenger on 45% of fares. Swept the class: `child_fare` had the same float, fixed too (ADR-0002).
10. **A lapsed hold could be handed straight back to its own passenger**, restarting the clock indefinitely.
11. **`HoldDesk` and `extend_hold` deleted** — a four-method pass-through with no caller, and hold extension the brief never asked for (it defeats AC1).
12. **Documents**: README rewritten for hold-then-confirm, the `hold_minutes` row, the waitlist rule and the fee; ADR index updated; A2 replaced.

## Rejected

- *Unify the error vocabulary* (`get`/`cancel` raise `KeyError`, `confirm` raises `HoldExpired`) — that's trunk's behaviour for an unknown ref, and telling "lapsed" from "never issued" means keeping a history of dead references.
- *`waitlist()` should place immediately when a space is free* — no criterion asks for it; the desk books in that case.
- *Reject a holds file whose bookings exceed capacity* (after a vessel swap) — negative availability just stops sales; choosing whose hold to drop is an operator policy call.

## Follow-ups (no tracker in this repo, so they're listed here)

- **A reference can still be reused after an unclean stop**: the counter is only persisted on `save_holds`, so references issued since the last save are reissued after a crash. Fixing it properly means reserving a block of references ahead of issuance.
- **A passenger who has confirmed can book a second space on the same sailing** — AC4 covers holds only. Replacing a *paid* booking silently would be worse, so this needs the brief to say what should happen.
- **Departed sailings are unguarded** (pre-existing): nothing compares against `sailing.departs`, so holds can be placed and promoted on a ship that has gone.

## Two things needing your call

- **The hold fee is computed but never charged or credited.** The brief's behaviour promises a credit on confirmation; criterion 6 only asks for the arithmetic, and nothing calls `pricing.hold_fee`. I wrote the README to say the ticket office applies it and Ferrybook keeps no money — correct if the till does it, wrong if you expected a ledger here. Also unspecified: a tenth of *which* fare, base or surged.
- **I could not update `.claude/skills/hold-ledger/SKILL.md`** — the sandbox denies writes under `.claude/skills`. Its `applies-to` still names `ferrybook/holds.py`, which this change deletes, so that lens would never select again. It should read `ferrybook/booking.py`.

The fixes are committed as `6f25cd3` on `feature-seat-holds`. When you have a reachable remote, the branch is ready to push and I'll open the PR.
