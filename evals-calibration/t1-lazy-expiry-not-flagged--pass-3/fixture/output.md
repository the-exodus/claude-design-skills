All five lenses reported; both ADR quotations check out verbatim. Branch baseline: 16 tests, green. The adversarial reviewer's throwaway file `tests/test_attack_holds.py` is in the working tree (18 tests, 15 red) — left uncommitted for you.

Triage below. Nothing fixed, as asked.

## Findings that hold — in scope, fix in this change

**1. `confirm` never settles, so a lapsed hold confirms** — `ferrybook/booking.py:83-88`
All five lenses, independently, with probes. `confirm` is the only operation that reads `_bookings` without `_settle()`; it infers lapse from the key being absent. Place a hold, advance 20 minutes, `confirm(ref)` → `status='confirmed'`, `held_until` in the past. Breaks AC2 and ADR-0003 verbatim ("Every public operation must settle first"). The suite's own AC2 test only passes because `tests/test_holds.py:47` pokes `available_cars` first. *Fix: `self._settle()` as the first statement; delete the masking line at :47 and :56.*

**2. `_promote` bypasses every check `book` makes** — `ferrybook/booking.py:50-59`
Adversarial and hold-ledger, with probes. `_promote` pops the queue head whatever space was released, and `_place` checks nothing: a lapsed *foot* hold promotes a *car* passenger onto a full deck (2 car holds on 1 space), it holds **reserved** car spaces under the shipped `reserved_car_spaces=2`, and it gives a second hold to a passenger who already holds (AC4). Breaks AC3, AC4 and the "reserved car spaces are never held" edge case. *Fix: promote through the checked path — match the released space's `vehicle` class, apply the same free-space computation, leave the entry queued when there's no room.*

**3. References are reused** — `ferrybook/booking.py:39-41`
Four lenses. `max(self._bookings, default=0) + 1`, with the comment "Keep references short: a settled hold gives its number back." ADR-0001 (Accepted, untouched by this diff) decides the opposite *in the same words*: "never issued again, even when that would keep references short." Probed: Ada's hold lapses, Bo is promoted onto ref 1, and Ada's printed ticket confirms Bo's hold — the exact ramp failure ADR-0001 exists to prevent. *Fix: restore trunk's monotonic `_next_ref` and persist it. If reuse is genuinely wanted it needs an ADR superseding 0001, not a code comment.*

**4. `make_book` never passes `hold_minutes`** — `ferrybook/booking.py:130-131`, `:31`
Five lenses. The shipped book keeps the constructor default of **30** minutes; probed `_hold_seconds == 1800` against `defaults.json`'s 15. AC1 holds only in the tests, which pass `hold_minutes=15` by hand — the production path is untested. *Fix: pass `settings["hold_minutes"]`; drop the 30 default so a missing key fails loudly.*

**5. A refused replacement destroys the hold the passenger had** — `ferrybook/booking.py:71-81`
Adversarial and hold-ledger. The dedupe loop deletes the existing hold *before* the capacity check, and matches on passenger+sailing while ignoring `vehicle`. Ada holds the last foot space, asks for a car on a full deck, gets `FullError`, and her foot hold is gone — released by none of the four paths, and not offered to the waitlist either. *Fix: check free space first (discounting the passenger's own row), delete only once placement will succeed, match on `vehicle`.*

**6. `available_cars` and `book` disagree about whether a hold occupies a space** — `ferrybook/booking.py:106-110` vs `:76`
Four lenses. `available_cars` counts confirmed only; `book` and `available_foot` count held+confirmed. The office screen offers a space `book` then refuses, and the ripple reaches `pricing.car_fare:11`: a fully-held car deck prices with **no surge**, contradicting README:13. *Fix: count `("held","confirmed")`. Side effect — the `test_a_booking_takes_a_car_space` rename at `tests/test_booking.py:8-11` reverts, since the original passes unchanged.*

**7. The hold fee is float money** — `ferrybook/pricing.py:24-26`
Four lenses. `round(fare * 0.1)` against ADR-0002: "never by multiplying by a float… Any float in a money calculation is a defect", and "Division rounds down, in the passenger's favour" — `round` is half-to-even, so it rounds *up* in the operator's favour on 45% of fares (probed: `hold_fee(15)` → 2 vs 1; 9995 → 1000 vs 999). The one test uses 42000, a clean multiple of ten, so it can't see it. *Fix: `fare * 10 // 100`; test a fare that isn't a multiple of ten.*

**8. The persisted deadline is a monotonic reading** — `ferrybook/booking.py:57`, `:116-121`, and `docs/design/assumptions.md` A2
Four lenses; documented and probed. The Python docs state `monotonic()`'s reference point is *undefined* and only differences are valid. On Linux it happens to be boot-relative (probed against `/proc/uptime`), which is why a service restart works — but after a host **reboot** a loaded hold lasts the previous uptime plus 15 minutes (probed: still held after 34 hours; space frozen until cancelled by hand), and the mirror case lapses every hold at startup. Suspend has the same effect. A2 states the guarantee unconditionally and this is the first code to lean on it in writing; its "how we would know" is also unobservable — a hold stuck for 34 hours looks idle, not alarming. The test can't see any of it because `tests/test_holds.py:73` hands the *same* `FakeClock` to the restarted book. *Fix: persist a wall-clock deadline; rewrite A2 to what's true and bounded; give the restart test a differently-based clock.*

**9. The restart path loses the waitlist, and `load_holds` overwrites live bookings** — `ferrybook/booking.py:116-127`
Adversarial, hold-ledger, platform reality. `_waitlist` is never persisted, so after a restart the first lapse releases a space to nobody and AC3 silently stops holding. `load_holds` does `self._bookings[booking.ref] = booking` with no collision check and no settle: probed, a walk-up booking taken before the file is read is replaced outright, its printed ref now naming someone else. `Booking(**row)` also trusts the file — an extra key raises `TypeError`, a missing one takes a dataclass default, and `held_until` defaults to `0.0`, i.e. *already lapsed*. *Fix: persist the waitlist and the ref counter; refuse a collision; settle after loading; pick fields explicitly.*

**10. `save_holds` truncates the only copy and never fsyncs** — `ferrybook/booking.py:120-121`
Platform reality (documented), adversarial. `open(path,"w")` truncates on open, and close doesn't imply fsync — a crash or kill during the pre-shutdown save loses *every* hold, which is precisely the moment AC5 covers. *Fix: temp file in the same directory, `flush()` + `os.fsync()`, then `os.replace()`.*

**11. `extend_hold` and `HoldDesk` are behaviour the brief never asked for** — `ferrybook/booking.py:90-92`, `ferrybook/holds.py:1-18`
Design parity, simplification, adversarial, hold-ledger. All four `HoldDesk` methods forward one call unchanged — a pass-through with no state, no decision, no production caller. `extend_hold` has no criterion, no test, defeats AC1 by letting any hold outlast `hold_minutes`, extends *confirmed* bookings happily, and raises bare `KeyError`. *Fix: delete both. A front-desk seam can arrive when it owns something.*

**12. README no longer describes the system** — `README.md:7`, `:19-23`
Design parity, adversarial, platform reality. "A booking is confirmed when it is made" is now false; so is "Cancelling a booking frees its space at once" (it hands the space to the waitlist as a hold). The `defaults.json` table omits `hold_minutes`, the very key AC1 names. *Fix: rewrite the Bookings section as built; add the table row.*

**13. The tests document the implementation, not the criteria** — `tests/test_holds.py:28-30`, `:47`, `:51-58`, `:67-74`
Design parity, platform reality, adversarial. `KeyError` from `get` is the dict's reaction, not a promise; the `available_cars()` prods exist only to hide finding 1; the waitlist test never asserts Bo actually holds the space; the restart test shares one clock and leaks `mkdtemp()`. *Fix: assert the documented behaviour; `TemporaryDirectory`; promote the three green `A9_ThingsThatHold` tests from the throwaway file.*

**14. Inconsistent signalling: `HoldExpired` for refs that never existed, `KeyError` for lapsed ones** — `ferrybook/booking.py:84-86`, `:92`, `:99`, `:104`
Design parity, hold-ledger, adversarial. `confirm(999)` on a never-issued ref raises `HoldExpired`; a lapsed ref raises `KeyError` from `get`/`cancel`. With finding 3 in play, a clerk can't tell "too late" from "wrong number". *Fix: one private settle-and-look-up used by all four.*

**15. `Booking`'s dataclass defaults make an undated booking born lapsed** — `ferrybook/booking.py:20-21`
Adversarial; simplification flagged the same thing. `status="held"`, `held_until=0.0` is what lets finding 9's silent-default path through. *Fix: make both required.*

**16. `waitlist` doesn't settle** — `ferrybook/booking.py:94-95`
Minor: it touches the queue, not the bookings, so ADR-0003's letter survives — but it's the same class as finding 1 and the fix is one line. *Fix for consistency.*

**17. A decision the build forced, with no record** — `docs/adr/`
Design parity, adversarial. The deadline's clock and the holds-file format is a real choice between alternatives (monotonic vs wall-clock, holds-only vs whole-book) that a later reader will want explained. *Fix: one ADR via `design:adr` once finding 8 lands. Findings 3 and 6 need no ADR if fixed as recommended; if either behaviour is intended, each needs one — 3 superseding ADR-0001.*

## Class sweep

I stated each holding defect as a pattern and searched the repo, inside the change and outside:

- **Settle-first omission:** exactly three — `confirm`, `waitlist`, `load_holds` (findings 1, 16, 9). All other public operations settle.
- **Float money:** `hold_fee` in the change, and **`child_fare` at `ferrybook/pricing.py:21`** (`int(foot_fare(route) * 0.5)`) outside it — same ADR-0002 violation. Pre-existing on trunk. `* 0.5` is exact in binary and `int()` truncates, so `// 2` is behaviour-identical: minor and mechanical, so by the skill's own rule it gets fixed here with the rest. No other float money anywhere.
- **Config key read by nothing:** only `hold_minutes`. `surge_threshold`/`surge_percent` reach `pricing.car_fare` directly; `reserved_car_spaces` is passed.
- **Invariants enforced in `book` but bypassed by writers to `_bookings`:** two — `_promote`→`_place` (finding 2) and `load_holds` (finding 9). The real fix for the class is to move the checks into `_place` so no path can skip them.
- **Persisted clock readings:** `held_until` is the only one. The timetable stores wall-clock ISO strings, so there's no second instance of finding 8.

## Rejected

- **`_settle` should use `<` rather than `<=`** (design parity, nit tail). A half-open interval is the standard reading of "a hold lasts 15 minutes", and expiring at the boundary errs toward releasing space. No criterion distinguishes them; this is a deliberate choice, not a defect.
- **Persist confirmed bookings too** (hold-ledger 7, adversarial 7). Real, but trunk persisted nothing at all, so a restart has always lost confirmed bookings — the change doesn't regress it, and AC5 names holds only. Whole-book persistence is a design question, not this branch's. → follow-up.

## Needs your call

**The hold fee is computed but never charged or credited** — `ferrybook/pricing.py:24` is its only mention; nothing calls it and `confirm` touches no money. The brief's behaviour paragraph says "credited on confirmation", but AC6 covers only the amount — which is why a bare pure function satisfies the acceptance list. There is no account, ledger or payment concept anywhere in the repo, so wiring this up is a new subsystem, not a fix. My recommendation: take it as a follow-up and let AC6 stand as the fee *calculation*, rather than growing a money-movement design inside this branch. Say the word if you'd rather have it in scope.

## Follow-ups (no tracker, per `AGENTS.md` — recorded here)

1. Whole-book persistence: confirmed bookings don't survive a restart (pre-existing; needs a decision about what the service saves).
2. Charging and crediting the hold fee — see above.
3. Nothing anywhere consults `sailing.departs`: holds can be placed on a sailing that has already sailed, and a later lapse promotes a waitlisted passenger onto a departed ship. Pre-existing for bookings on trunk, but holds add a new way to allocate space on a gone ship — and it's on the repo's own attack list. Needs design.

## Where this leaves the branch

Nine of your six acceptance criteria-worth of promises are broken on the path a user actually runs: AC1 (finding 4), AC2 (1), AC3 (2, 9), AC4 (2, 5), AC5 (8, 9, 10), AC6 (7), plus the reserved-spaces edge case (2) — and three standing ADRs are contradicted (0001, 0002, 0003). I'd fix 1–10 before the PR; 11–17 are cheap and in the same files. No lens was skipped: you gave no lens argument, so the table chose, and `ferry-attacks` and `hold-ledger` were both selected by path.

The throwaway `tests/test_attack_holds.py` is your red-test harness for most of 1–10 — 15 failing tests to promote under proper names as you fix, and 3 green ones worth keeping. Delete the file once they're moved.
