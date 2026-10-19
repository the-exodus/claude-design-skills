# Answer key: code-style-lockerline

Lockerline, an invented parcel-locker network in Java. 30 planted comments: 21 keeps, 4 deletes, 5 shrinks, so the common case is keep, as it was in Tileand's own pass (THE-221). `AGENTS.md` sets three citation regimes: `src/` may cite ADRs by number; `tests/` cites none, and a pointer-only comment there is removed; `tests/architecture/` may cite the ADR it protects beside its own words.

A regression fixture: iterate the skill against it. `code-style-heldout-cinder` is the held-out one.

## Keeps

| File | Comment (start) | Why it stays |
|---|---|---|
| `StatusCodes` | class: "The integers the courier app reads…" | says what no signature can; its citation is allowed in `src/` |
| `CompartmentSize` | "Door heights of 9, 19 and 39 cm…" | facts from outside the code |
| `Compartment` | `collectionCode`: "Held only until the door is opened…" | why it is cleared |
| `LockBoard` | `release`: "The board answers ACK before the solenoid…" | platform fact |
| `CompartmentController` | class: "Runs on the lock board's own thread… (ADR-0001)" | thread contract, cited decision |
| `CompartmentController` | `run`: "Polls every 200 ms: the board raises no interrupt…" | platform fact |
| `CompartmentController` | trailing on `sleep(40)` | the only record of why 40 ms |
| `LockerBank` | class: "One cabinet at one site…" | which thread state changes on |
| `LockerBank` | trailing on `ledger` | an invariant another class holds |
| `LockerBank` | `completeDropOff`: "The tail of every drop-off the bank accepts…" | **trap**: "the bank accepts" looks like it restates the method; it is the qualifier excluding refused drop-offs, which return early and never reach it |
| `LockerBank` | trailing on `failed >= 3`: "three tries, as the printed receipt promises" | **trap**: looks like it restates the 3; it is the only record of why |
| `CollectionCodes` | trailing on `ALPHABET` | why these characters |
| `CollectionCodes` | `LENGTH`: "Six characters: the scanner's keypad fallback…" | a field trial and a timeout |
| `DwellPolicy` | `LIMIT_DAYS` | the receipt's promise and the 06:00 round |
| `DwellPolicy` | `dwellDays`: "Counted in local calendar days… (ADR-0004)" | the counting rule, cited |
| `ReservationLedger` | `lock` | why the lock spans both steps |
| `FakeLockBoard` | class | fixture description beside the fake |
| `DwellPolicyTest` | on the field: "The bank's zone; clocks go forward on 2026-03-29…" | zone fact |
| `DwellPolicyTest` | trailing "23:59:59 at the site" | the instant in the site's zone |
| `LockerBankTest` | trailing "only the courier's release; no scan opened the door" | why the count is one |
| `ControllerIsolationTest` | "The controller never reaches the courier API… (ADR-0001)…" | `tests/architecture/` may cite beside its own words; also says what the check cannot see |

## Deletes

| File | Comment | Why |
|---|---|---|
| `Compartment` | `size()`: "Returns the compartment's size." | restates the getter |
| `LockerBankTest` | class summary: "A drop-off is accepted only into…" | a specification restated in a test file; under `tests/` no pointer may replace it |
| `LockerBankTest` | "Arrange a bank with one empty small compartment" | restates the next line |
| `CollectionCodes` | "See ADR-0003." | only points at a record; a citation never stands in for a claim, and the reason is already on `onCodeScanned` |

## Shrinks

| File | Cut | Keep | Watch for |
|---|---|---|---|
| `BankListener.onDoorLatched` | "The door has latched and", ideally; leaving it is no fault (owner, 2026-10-19: in proportion), so it is not graded | after the debounce; dwell clock from now, not the scan; lock-board thread | the contract's three parts all survive |
| `StatusCodes.HELD_FOR_INSPECTION` | the re-listing "0 (empty) … 5 (fault)" | distinct from the others, so the courier app can tell an inspection from a fault | "distinct" must keep something to be distinct from |
| `LockerBank.onCodeScanned` | "A collection code was scanned at the bank" | constant time, and why | **trap**: "it is compared…" loses its antecedent unless repaired |
| `FanOutListener` | "Forwards each event to several listeners" | "used to mirror … to the support console while an engineer is attached" | **trap**: as a *what* ("Mirrors … to the support console") it is false; the class knows no console |
| `LockerBankTest` trailing | "(ADR-0004)", and "The clock starts at the latch, not the scan" if the run sees that it restates the test's name | nothing need stay: the two instants in view show the scan two minutes before the latch, so deleting the whole comment is also right | the citation goes by `tests/`' convention; only that is graded |

## Naming

The prompt asks for no renames. `DwellPolicy`, `CompartmentId`, `Compartment`, `returnToSender` and `onDoorLatched` carry lexicon words and must stay.

## Graders

- `keep-*`: one regex per kept comment (two for those with a citation), on a distinctive phrase, tolerant of reflow across Javadoc lines.
- `gone-*`: one regex per delete.
- `shrink-*-cut` and `shrink-*`: the local half gone, the non-local half present.
- `lockerline-shrink-*`: one llm grader per shrink whose wording can break, re-reading the surviving text on its own. The test-file citation drop has none: what survives is the original sentence less its parenthesis.
- `lockerline-nothing-added`: one llm grader on `LockerBank.java`, the file with the most comments at risk.
- `name-*-kept`: the domain identifiers' declarations.

Ungraded: whether a run also tidies the `CompartmentController` and `LockerBank` class summaries' wording without changing their claims; anything the prompt did not ask for in `docs/`.

The regex graders were checked against the fixture (every `gone` and `cut` fails, every keep passes) and against a hand-made correct tidy (all pass).
