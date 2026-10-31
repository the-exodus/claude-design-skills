# Answer key: the ferry fixture

Ferrybook, an invented car-ferry booking service in Python with stdlib `unittest`. `build.sh` commits `base/` on `trunk` (with a fake `origin/HEAD` naming `trunk` as the remote's default branch) and an overlay on a branch. The tests pass on `trunk` and on every branch. Nothing here is real, so it can be committed. It is a regression fixture: fair to iterate the skill against. The held-out fixture is `review-heldout-quarry`.

The base carries three repo lenses under `.claude/skills/`, each with a phrase found nowhere else so a grader can see where its body went:

| Lens | Declared | Matches on `feature` | on `fix` | Marker |
|---|---|---|---|---|
| `ferry-attacks` | `extends: adversarial`, `ferrybook/**` | yes | yes | "departure passes while bookings or holds" |
| `hold-ledger` | own, `ferrybook/holds.py` | yes (the branch adds it) | no | "exactly one release path" |
| `manifest-export` | own, `ferrybook/manifest/**` | no | no | "port authority manifest" |

## `feature` (branch `feature-seat-holds`): seat holds

Used by `cycle-feature`, `lens-ferry` and the trigger cases. Signals: a feature with new interface surface (`HoldDesk`, `confirm`, `extend_hold`, `waitlist`, `save_holds`, `load_holds`), and it relies on `time.monotonic` across a restart, which assumption A2 covers. So all four built-in lenses run, plus `ferry-attacks` (with adversarial) and `hold-ledger` (its own reviewer).

| Id | Where | What is wrong | Lens that should find it |
|---|---|---|---|
| D1 | `booking.py` `_new_ref` | `max(self._bookings) + 1` gives a settled or cancelled hold's reference back: cancel ref 2, the next booking is ref 2 again. ADR-0001. No comment points at it: an earlier version said "Keep references short", echoing the alternative ADR-0001 rejected, and a run spotted it while only gathering context. | design parity, adversarial |
| D2 | `booking.py` `confirm` | does not settle first, so a hold whose time has passed is confirmed when no operation ran since it lapsed. Criterion 2; ADR-0003's consequence says every public operation settles first. | adversarial |
| D3 | `booking.py` `available_cars` | now counts only confirmed bookings; `pricing.car_fare`'s surge still reads it as "spaces left to sell", so surge is under-applied while holds are open. | adversarial (ripple) |
| D4 | `pricing.py` `hold_fee` | `round(fare * 0.1)`: a float in money, against ADR-0002. | design parity |
| D5 | `README.md` | still says "A booking is confirmed when it is made"; the configuration table has no `hold_minutes`. | design parity |
| D6 | `booking.py` `make_book` | does not pass `hold_minutes`, so the shipped book holds for the constructor's 30 minutes, not `defaults.json`'s 15. Tests use the constructor. Criterion 1 under the shipped configuration. | adversarial (via `ferry-attacks`) |
| D7 | `booking.py` `extend_hold`, `holds.py` `extend` | behaviour the brief did not ask for. | design parity (scope) |
| D8 | `holds.py` `HoldDesk` | only forwards to `BookingBook`. | simplification |
| D9 | `booking.py` `save_holds` / `load_holds` | persist `time.monotonic` deadlines, but the Python documentation says its reference point is undefined and only differences within a process are valid. Assumption A2 is wrong too. Criterion 5. | platform reality |

Outside the change, for the class sweep: `pricing.child_fare` computes `int(foot_fare(route) * 0.5)`, the same float-in-money class as D4. It is minor and mechanical (`// 2` gives the same results), so under the cycle's default policy it is fixed in the PR.

Traps, correct as written:

| Id | What looks wrong | Why it is right |
|---|---|---|
| T1 | No timer or thread expires holds; lapsed holds linger in memory. | ADR-0003 decides lazy settlement. (D2 is a different finding: one operation that forgets to settle.) |
| T2 | A passenger's second hold silently replaces the first. | Brief, criterion 4. |

## `fix` (branch `fix-midnight-departures`), with the `policy` overlay on the base

Used by `cycle-fix-defers`. One function changed, no interface: adversarial and design parity only; `ferry-attacks` matches, `hold-ledger` does not; nothing the assumptions record covers.

- The fix is itself off by one: `day_start < s.departs < day_end` drops a midnight sailing from its own day too. Correct: `day_start <= s.departs < day_end`.
- The class sweep finds the same inclusive end bound in `arrivals_on`, outside the brief. The `policy` overlay's `AGENTS.md` says such defects are never fixed in the change, only listed as follow-ups, so `arrivals_on` must stay as it is and be named in the report.

## `fix,protected-fix` (branch `fix-midnight-departures`), with the `protected` overlay on the base

Used by `cycle-protected-trace`; no other case sees these overlays. `protected` adds `.claude/protected-paths.txt` on `trunk` (itself, `.claude/settings.json`, `.claude/skills/**`, `docs/adr/**`). `protected-fix` goes on top of `fix` and changes three protected paths. The case's brief carries a batch of provisional closures with the maintainer's answers.

| Path | Closure | Expected |
|---|---|---|
| `.claude/skills/ferry-attacks/SKILL.md` (a midnight-boundary attack added) | P1, approved | traced to P1; never a finding |
| `docs/adr/0004-a-day-runs-from-midnight-to-midnight.md` (new, correct as a record) | P2, declined | `Protected change without an approved closure: <path>`, needs the author |
| `docs/adr/README.md` (the index row for 0004) | P2, declined | the same |

The `fix` defects above still apply: the off-by-one, and `arrivals_on` for the sweep (no `policy` overlay here, so the default out-of-scope rule). ADR-0004 states `day_start <= t < day_end`, which the branch's code breaks, so design parity may also report the code against the record; that is right and nothing grades it.

## `records` (branch `adr-refunds`)

Used by `cycle-records-only`. Only an ADR is added: design parity in records-only mode, no suite.

- ADR-0004 computes refunds as `round(paid / 100 * 0.8)` in kroner, contradicting accepted ADR-0002 (integer øre, no floats) without superseding it.
- The ADR index in `docs/adr/README.md` has no row for 0004 (the brief's criterion 2).
- The brief contradicts itself: criterion 3 cites a criterion 5 that does not exist, and its edge case says "refund window" where the behaviour says "cancellation window".

## What the graders do not check

- That D1 to D9 are all found in `cycle-feature`: the lens case `lens-ferry` grades the findings; `cycle-feature` grades the selection, the fixes of D1, D2 and D4, and the sweep.
- D3, D5 to D9 being fixed in `cycle-feature`: several have more than one right fix.
- The test-first grader is satisfied by any test file written before the first fix, including an adversarial reviewer's throwaway test. It catches a session that edits source before writing any test at all.
