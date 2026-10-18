All five reviewers came back; the branch is green (16 tests) and every reviewer confirmed that before starting. Overlap was heavy — 42 raw findings merged to 21. Triage below; I changed nothing.

## Must fix in this change — acceptance criteria not met

**1. `confirm` never settles, so a lapsed hold confirms fine — AC2 is not met.** `ferrybook/booking.py:83` is the only mutator without `_settle()`, against ADR-0003's "every public operation must settle first". Proven red: hold placed, clock +60 min, `confirm` returns `status="confirmed"`. `tests/test_holds.py:44` passes only because it wedges `book.available_cars("S1")` in first to settle on `confirm`'s behalf.
→ **Fix.** `self._settle()` as the first line of `confirm`; drop the nudge from the test. All four code lenses found this independently.

**2. `make_book` ignores `hold_minutes`, so the shipped config has no effect — AC1 is not met.** `booking.py:131` passes only `reserved_car_spaces`; the constructor default is `30` (`booking.py:31`). Probed: `make_book(sailings, config.load())._hold_seconds == 1800` while `defaults.json` says 15. Every real hold is twice the configured length; only the tests, which pass `hold_minutes=15` by hand, see 15.
→ **Fix.** Pass `settings["hold_minutes"]`, and make the constructor default 15 or remove it.

**3. `_new_ref` reuses references, reversing ADR-0001 with no superseding record.** `booking.py:39-41`, comment and all ("a settled hold gives its number back") — the alternative ADR-0001 explicitly rejected. Proven: Ada's hold lapses, Bo books and gets ref 1 again, and Ada's printed ticket `confirm(1)` confirms **Bo's** hold. `tests/test_booking.py:26` misses it because both bookings are live in that test.
→ **Fix** the code, not the record: restore the monotonic `_next_ref`, and raise it past loaded refs in `load_holds`.

**4. `_promote` places a hold with no capacity, reserved-space or travel-type check — oversell.** `booking.py:50-59` pops the waitlist head and calls `_place` directly, bypassing everything `book` checks. Proven: a *foot* hold lapsing promotes a *car* waitlister onto a sailing with `car_spaces=2, reserved_car_spaces=2` — a reserved space, which the brief says is never held; and promotion can exceed total car spaces. Live under the shipped defaults.
→ **Fix.** Route promotion through the same free-space path as `book`, filtering the queue by travel type.

**5. The waitlist bypasses "one hold per sailing" — AC4.** The replace rule lives in `book` (`booking.py:71-73`), not in `_place`, and `waitlist` (`booking.py:94`) de-duplicates nothing. Proven: waitlist the same passenger twice, two holds lapse in one `_settle`, two concurrent holds for one passenger.
→ **Fix.** Move the replace step into `_place`, and ignore a `waitlist` call for a passenger already queued or holding on that sailing.

**6. `available_cars` changed meaning and now contradicts `book`, `available_foot` and the surge rule.** `booking.py:106-110` counts `("confirmed",)` only; `book` and `available_foot` count `("held","confirmed")`. Ripple: `pricing.car_fare:11` feeds `available_cars` into the surge threshold, so a sailing held out prices as empty (proven: 6 spaces, 2 held → 42000 instead of 50400), and the reader advertises a space `book` refuses. The diff rewrote `tests/test_booking.py:8` to insert a `confirm` so the old assertion kept passing.
→ **Fix.** Count `("held","confirmed")` as everywhere else and revert that test to its trunk form. If "spaces a customer might still get" is genuinely wanted, that's a second, differently-named reader plus an ADR — the surge rule must keep the sellable count.

**7. Persisted deadlines are `time.monotonic()` values, which don't survive the restart they exist for — AC5, and assumption A2 is false as written.** `booking.py:117` cites A2; A2 claims monotonic values "stay valid across restarts of the service". The Python docs state the reference point is **undefined**; on Linux it's `CLOCK_MONOTONIC`, probed equal to `/proc/uptime` on this host — it resets on reboot and stops during suspend. Both directions probed: reload after a reboot and a 15-minute hold lives ~34 hours; reload into a shorter boot and it's deleted instantly, the space handed to the waitlist with no error.
→ **Fix.** Persist a wall-clock instant (convert at the save/load boundary, keep the injected monotonic clock for settling), and supersede A2 to say monotonic differences are valid within one boot and nothing monotonic may be persisted. Ranked top by platform reality.

**8. `load_holds` destroys live bookings, never settles, and crashes on a first start.** `booking.py:123-127` assigns by ref into a dict that may already have entries (proven: a booking taken since startup is silently overwritten), skips `_settle` so holds that lapsed while the service was down are observable, and raises `FileNotFoundError` when there is no holds file yet.
→ **Fix.** Missing file means no holds; refuse a colliding ref; `_settle()` after loading.

**9. The waitlist doesn't survive the restart that holds do — AC3 after AC5.** `save_holds` writes `_bookings` only; `_waitlist` is dropped, so after a restart a released space goes to walk-up trade and the queued passenger waits forever.
→ **Fix.** Persist both in one file.

**10. `hold_fee` uses float arithmetic — ADR-0002.** `pricing.py:26`, `round(fare * 0.1)`: float multiplication plus documented round-half-**even**, where the ADR requires `amount * percent // 100` and rounding down in the passenger's favour. Proven: `hold_fee(15) == 2` vs `15 // 10 == 1`; `hold_fee(5) == 0` but `hold_fee(15) == 2` — ties break inconsistently. Latent only because every current fare is a multiple of 10, which is also why the one test (42000) can't see it.
→ **Fix.** `fare // 10`, and test a fare that isn't a multiple of ten.

**11. The hold fee is charged by nothing and credited by nothing — AC6's behaviour is unbuilt.** `pricing.hold_fee` has no caller outside its own test; no `Booking` field records a fee, `book` doesn't charge, `confirm` doesn't credit.
→ **Fix, and it needs one decision from you:** Ferrybook has no money ledger at all today, so "credited on confirmation" needs somewhere to live (simplest: a `fee` field on `Booking`, zeroed on confirm). It's inside the brief, so I'd build it here rather than defer — see the question at the end about what happens to the fee when a hold lapses.

## Must fix — smaller, same scope

**12. A refused replacement leaves the passenger with neither hold.** `booking.py:71-80` deletes the earlier hold *before* the capacity check, so `FullError` destroys a hold and places nothing — and doesn't promote the freed space either. → Compute `free` with the replaced refs subtracted, raise before deleting.

**13. Replacing a hold strands the released space.** Same lines: the replace loop matches any hold for that passenger, including the other travel type, and never calls `_promote`. Ada swapping a car hold for a foot one frees a car space the queue never sees. → `_promote` after the replacement is placed.

**14. `cancel` and `extend_hold` on a just-lapsed hold raise a bare `KeyError`.** `booking.py:92,99` settle first — deleting the very hold the caller named — then index it; `HoldDesk` passes it straight through. AC3 covers cancelling. → Raise `HoldExpired(ref)`, or make cancelling an already-released hold a no-op. (`get` raising `KeyError` is deliberate and asserted by your test — leaving that.)

**15. `extend_hold` / `HoldDesk.extend` is behaviour the brief didn't ask for and it defeats AC1.** `booking.py:90`, `holds.py:14`: unbounded, unrecorded, untested, extends confirmed bookings too. → Remove both (design parity and simplification agreed).

**16. `HoldDesk` is a pass-through module.** All four methods forward unchanged; its only caller is its own test. The design philosophy's rule against pass-through layers applies squarely. → Delete `ferrybook/holds.py` and its test. (This retires the repo's `hold-ledger` lens target, worth noting.)

**17. The user reference describes the pre-hold system.** `README.md:7` "A booking is confirmed when it is made" is now false; the `defaults.json` table has no `hold_minutes` row; nothing documents holds, lapsing, the waitlist or the fee. → Rewrite the Bookings paragraph, add the row and a fee sentence.

**18. Three of the branch's own tests pass for the wrong reason.** `tests/test_holds.py:44` (the settle nudge, finding 1), `:73` (hands the "restarted" book the *same* `FakeClock` — the one thing a restart cannot preserve, so AC5's test structurally cannot fail, finding 7), and `:50-56` (asserts only that a third passenger gets `FullError`, never that Bo actually holds the space AC3 promises). → Rewrite all three; give `FakeClock` a way to change its origin.

**19. [nit] `Booking`'s field defaults build an already-lapsed hold.** `booking.py:20-21`: `status="held", held_until=0.0`, so any four-arg `Booking(...)` dies at the next settle. → Make them required, or default `status="confirmed"`.

## Class sweep

Stating each held defect as a pattern and searching the whole repo, inside the change and out:

- **Public operation that doesn't settle (ADR-0003):** `confirm` (1), `load_holds` (8), and `waitlist` (`booking.py:94`). `waitlist` only appends, so it observes nothing lapsed — harmless today, but it's the same omission; add the call for the rule's sake.
- **A hold created without the capacity path:** `book` checks; `_promote` (4) and `_load_holds` (8) don't. Three creation sites, one check.
- **Float in a money calculation (ADR-0002):** `hold_fee` (10, in the change) and **`child_fare` at `pricing.py:21`, `int(foot_fare(route) * 0.5)` — pre-existing on trunk, outside the brief.** Truncation happens to match the ADR's "round down", so no behaviour changes; it's a one-line mechanical fix to `foot_fare(route) // 2`. → I'd fix it in this change under the minor-and-mechanical rule, with a test.
- **Reference uniqueness:** `_new_ref` (3) and `load_holds`' unguarded assignment (8) are one defect in two places.

## Follow-ups — outside the brief, need design or are large

- **`save_holds` isn't atomic or durable.** `open(path,"w")` truncates before writing, so a kill mid-write leaves the only copy of the holds half-written, and `load_holds` then raises an uncaught `JSONDecodeError` (both states probed). Fix is the documented `tmp` + `flush`/`fsync` + `os.replace` pattern plus a decision on what a corrupt file should do — that last part is a behaviour decision, so: **follow-up**, not this PR. The missing-file case is in scope and is part of finding 8.
- **Confirmed bookings don't survive a restart at all.** `save_holds` filters to `status == "held"`, so after a reload every sold space reads free. Trunk had no persistence whatsoever, so this is not a regression, and the brief asks only that holds survive — but with a durable store now half-present it's a sharp edge. **Follow-up:** where confirmed bookings live needs a decision.
- **Nothing compares against `Sailing.departs`.** A hold can be placed, or handed to a waitlister by `_promote`, on a sailing that has already sailed; `tests/helpers.py` defaults to a past date, so the whole suite books departed sailings. Pre-existing for `book`; promotion is a new way in. **Follow-up.**
- **[nit] ADR-0003's filename says "holds-and-expiry-are-settled-lazily" while its title and index line say "Expiry is settled lazily, never by a timer".** Pre-existing, cosmetic. **Follow-up.**
- **[nit] `tests/test_holds.py:71` leaks a `mkdtemp` directory per run.** → `TemporaryDirectory` or `addCleanup`. Mechanical; fold into the test rewrite (18).

## Rejected

- **A versioned `{"version": 1, "holds": [...]}` envelope for the hold file** (platform reality, nit). Real but speculative: no migration need the brief names, and it trades one complexity for another while the format question is still open under finding 7. Rejected as scope expansion — revisit if the persistence follow-up lands.
- **Weakening `_taken`'s `statuses` parameter away entirely** (simplification's variant of finding 6). The simplification reviewer argued a settled book holds nothing lapsed, so the status filter is dead weight. It isn't: `save_holds` needs the held/confirmed distinction, and finding 11 will need it too. Taking the agreed half — making `available_cars` match `available_foot` — and rejecting the parameter removal.

## Records to write

Findings 3 and 6 both tempt a decision record; both should be fixed in code instead, so neither needs one. Two genuinely do:
- **A2 superseded** in `docs/design/assumptions.md` (finding 7), with "how we would know: after a host reboot, reloaded holds never lapse".
- **A new ADR for the persisted-deadline clock** — moving the hold deadline onto a wall clock while settling on a monotonic one is a real choice between alternatives (and brings NTP adjustment with it) that a later reader will want explained. Write it through `design:adr`.

## Two things I need from you

1. **What happens to the hold fee when a hold lapses or is cancelled** — kept, refunded, or never taken? The brief covers only the credit on confirmation, and finding 11 can't be built without it.
2. **The waitlist** appears in AC3 but nowhere in the brief's Behaviour paragraph, yet the change had to add a public `waitlist` method. Confirm it's in scope for this PR, or it's a second feature riding along.

## Housekeeping

The adversarial reviewer left six throwaway files in the working tree, uncommitted: `tests/test_attack_{refs,confirm,waitlist,restart,defaults,availability}.py` (20 assertions, 19 red). **`python3 -m unittest` is now 36 tests with 18 failures and 1 error until you deal with them** — the 16 committed tests still pass on their own. They're the red proofs for findings 1–11; I'd promote the ones covering 1, 3, 4, 7, 8 and 10 under proper names and delete the rest.

Stopping here as asked — no fixes, no re-run round, nothing committed. There's no issue tracker (AGENTS.md), so this report is the record.
