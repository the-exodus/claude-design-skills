# code-style-heldout-cinder: answer key

Cinder is a small Rust controller for an electric pottery kiln (MAX31855 thermocouple amplifier over SPI, zero-crossing solid-state relay). The agent is asked to tidy the comments before a handover, directly, without renaming or changing behaviour. The fixture has 31 comments: 23 keep, 8 change (5 deletes, 2 shrinks, 1 citation drop). The rule being tested is locality: what the name, signature and code in view already say goes; what lives elsewhere (hardware, platform, a decision record, an invariant another type guards, a caller contract, a why) stays; a mixed comment is shrunk to its non-local part without breaking what remains.

Kinds are numbered as in the brief: 1 restatement, 2 restating + contract, 3 restating + rationale with a duplicated enumeration, 4 platform/hardware fact, 5 rationale, 6 invariant guarded elsewhere, 7 test restating a recorded spec, 8 test fixture description, 9 looks redundant but is the only record of why, 10a/b/c shrink traps (qualifier, antecedent, why-clause), 11(i)-(iv) citations, 12 glossary terms.

## Planted comments

### src/temperature.rs

| Line | Original | Kind | Answer | Why |
|---|---|---|---|---|
| 3-5 | A temperature in quarter-degrees Celsius. The thermocouple amplifier resolves 0.25 °C, so every reading is a whole number of quarter-degrees and arithmetic on them is exact (0001). | 4, 11(ii) | keep (cutting the first sentence is tolerated; nothing in the rest depends on it) | The amplifier's resolution is a hardware fact; the claim carries its own citation, which `src/` may have. |
| 18 | Returns the raw quarter-degree count. | 1 | delete | `raw(self) -> i32` on `QuarterDegrees` says exactly this. |

### src/thermocouple.rs

| Line | Original | Kind | Answer | Why |
|---|---|---|---|---|
| 16-18 | The hot-junction temperature is a 14-bit two's-complement field in bits 31..18. Bit 16 is set whenever any of the three fault bits (2..0) is set, and the temperature field means nothing in that case. | 4 | keep | The chip's frame layout; the code's masks and shifts are meaningless without it. |
| 27 | Shift as i32 so that the arithmetic shift carries the sign bit down. | 5 | keep | Why the cast precedes the shift; dropping the cast silently breaks negative readings. |
| 41-43 | The chip converts continuously and takes about 100 ms per conversion; reading faster than that returns the previous result again, not a fresh one. | 4 | keep | Chip timing, nowhere in the code. |

### src/relay.rs

| Line | Original | Kind | Answer | Why |
|---|---|---|---|---|
| 8-10 | Shortest on-time worth commanding. The relay is a zero-crossing type and only switches at the next zero crossing of the mains, so anything shorter than a half-cycle at 50 Hz is either lost or stretched to one. | 4 | keep | Hardware behaviour that explains the 10 ms value. |
| 20-21 | Drive the pin low first: it powers up floating, and the relay input reads a floating pin as on. | 9 | keep | `pin.set_low()` in a constructor looks like obvious initialisation; the comment is the only record that skipping it switches the elements on. |
| 26 | Sets the relay on or off. | 1 | delete | `set(&mut self, on: bool)` on `Relay`. |

### src/schedule.rs

| Line | Original | Kind | Answer | Why |
|---|---|---|---|---|
| 5-6 | The kiln's rated maximum. The elements are rated higher, but the lid brick is not. | 9 | keep | The only record of why the limit is 1300 °C rather than the element rating; 0004 states the limit exists, not why. |
| 11 | One ramp-and-soak step of a schedule. | 12 | keep | Correct use of the glossary's words; the meaning of Segment is not in the code. |
| 14-16 | Quarter-degrees per hour. Positive heats and negative cools; never zero, and the sign must agree with the direction from the previous segment's target to this one's. `Schedule::new` checks both. | 6 | keep | Unit of a bare `i32`, and an invariant another type enforces. |
| 38-39 | Checks a schedule once, at load, so that the controller can follow it without re-checking anything (0004). | 11(ii), 5 | keep | A why plus its record citation. |
| 68 | Returns the schedule's segments. | 1 | delete | `segments(&self) -> &[Segment]`. |
| 73-74 | Planned duration of the heating segments, ramps plus soaks, for a kiln starting at `from`. The display's end-time estimate is built on it. | 10a | keep "of the heating segments" (cutting "ramps plus soaks" / "for a kiln starting at `from`" is fine) | Looks like a restatement of `planned_duration`, but "heating segments" limits it to the `take_while` the code does; without it the doc claims the whole schedule. The display sentence is a caller fact from elsewhere. |
| 88-91 | A cone a preset can fire to: 06, 04, 5, 6 or 10. Cones are an enum rather than plain numbers so that a preset cannot name a cone with no known peak: `peak` matches every variant, so a cone added without its temperature fails to compile. | 3 | shrink: drop ": 06, 04, 5, 6 or 10" (and optionally the restating "A cone a preset can fire to"), keep the rationale | The list duplicates the variants and the match and rots when a cone is added; the why lives nowhere else. |
| 102 | Peak temperature at a 60 °C/h final ramp, from the cone maker's chart. | 4, 12 | keep | Provenance and conditions of the numbers; external fact, uses Cone correctly. |

### src/controller.rs

| Line | Original | Kind | Answer | Why |
|---|---|---|---|---|
| 9 | See 0002. | 11(i) | delete | A pointer with no claim of its own on `WINDOW`. |
| 30-31 | `Instant` stops while the Pi is suspended on Linux, so a suspend pauses the schedule instead of jumping it forward. | 4 | keep | Platform clock behaviour the schedule depends on. |
| 57-58 | One firing of a schedule, from switch-on to the end of its last segment's soak. | 12 | keep | Correct use of glossary terms; scope of the type. |
| 74 | `Schedule::new` rejects an empty schedule, so there is a first segment. | 6 | keep | Why `segments()[0]` cannot panic; guarded in another file. |
| 91-94 | Runs one control window: reads the thermocouple, sets the relay for the window's duty and sleeps until the window ends. Call it again as soon as it returns: the relay is off between calls but the schedule's clock is not, so a slow caller leaves the kiln behind its schedule. | 2 | shrink: cut the narration after "Runs one control window" (a bare "Runs one control window." may stay), keep the contract | The narration is the body in view; the caller contract is not in view anywhere. Surviving text must stand alone: "Call it again as soon as it returns: ..." does. |
| 104-106 | Soak time is counted from when the kiln first reaches the target, not from when the ramp's planned time runs out, so a ramp the elements could not keep up with still gets its full soak. | 5 | keep | Rationale for a non-obvious choice. |
| 124-127 | The same duty calculation serves cooling segments. It keeps the relay off above about 700 °C, because the kiln sheds heat faster than any rate a schedule asks for, and fires the elements below that to slow the fall. | 10c | keep (at least: the 700 °C claim never without its reason) | Nothing in the code mentions 700 °C; without the "because" clause the sentence reads as a threshold in code, which is false. |
| 144-146 | Takes the next reading from the thermocouple and folds it into the fault count. Three in a row abort the firing (0003); a good reading resets it, and a fault short of the third reports the last good temperature instead. | 10b, 11(ii) | keep whole, or cut the first sentence only while repairing the references ("Three consecutive faults ...; a good reading resets the count") | The first sentence looks like a restatement but introduces "the fault count"; cut naively, "Three in a row" has no noun and "resets it" reads as resetting the firing. |

### tests/

| Location | Original | Kind | Answer | Why |
|---|---|---|---|---|
| tests/controller_test.rs:10-12 | The bench kiln gains 2 °C for every second the relay is on and loses 1 °C for every second it is off, so it can always outrun the schedule: these tests see what the controller does, not what a slow kiln does. | 8 | keep | Describes the fake in `tests/support/` and what the tests therefore do and do not cover. |
| tests/controller_test.rs:64-65 | A firing aborts on the third consecutive fault, and a good reading in between starts the count again. | 7 | delete | Restates 0003; the test name and frames say the same. AGENTS.md forbids citing in tests, so it must not be re-sourced either. A line left in its place that describes what the test's frames or harness are doing, rather than restating the abort rule, is acceptable. |
| tests/thermocouple_test.rs:4-5 | Frames captured from the studio kiln's amplifier: probe at room temperature, probe in boiling water, and probe unplugged. | 8 | keep | Provenance of the hex constants, not derivable from them. |
| tests/schedule_test.rs:58-59 | A preset whose cone peaked above the limit would be rejected at load and `preset` would panic on it, so every peak has to stay under the limit (0004). | 11(iii) | keep the claim, drop "(0004)" | Tests never cite records (AGENTS.md); the claim is about `preset`'s `expect`, which is not in view. |
| tests/architecture/main.rs:6-7 | Paths are relative to the crate root, which is the working directory cargo runs integration tests in. | 4 | keep | Tooling behaviour the relative `"src"` path depends on. |
| tests/architecture/layering.rs:3-4 | No public function in `src/` takes or returns a float: temperatures cross module boundaries as `QuarterDegrees` (0001). | 11(iv) | keep whole | Structural-rule folder: a citation beside its own claim is allowed. |
| tests/architecture/layering.rs:20-21 | Only `relay.rs` calls `set_high` or `set_low`, so nothing switches the elements except through `Relay` (0002). | 11(iv) | keep whole | As above. |

### Glossary identifiers (kind 12)

`Firing`, `Segment`, `soak`, `Cone`, `WINDOW` (glossary: Firing, Segment, Soak, Cone, Window, Duty). None is to be renamed; "soak" in particular invites "hold" and `Firing` invites `Run`.

## Counts

- 31 comments. By verdict: 23 keep (including the three shrink traps and the 11(iv) pair), 5 delete (3 x kind 1, 11(i), kind 7), 2 shrink (kinds 2 and 3), 1 citation dropped with claim kept (11(iii)).
- By primary kind: 1 x3, 2 x1, 3 x1, 4 x6, 5 x2, 6 x2, 7 x1, 8 x2, 9 x2, 10a/b/c x1 each, 11(i) x1, 11(ii) x2 (temperature.rs, Schedule::new; take_reading's citation makes a third, filed under 10b), 11(iii) x1, 11(iv) x2, 12 x2 comments (Cone::peak also uses a term) + 5 identifiers.

## What the graders check (50)

- 18 `cinder-keep-*` regexes: each kept comment's distinctive phrase is still present.
- 3 trap regexes and 3 trap llm graders (`cinder-trap-*`): the qualifier "heating segments"; the abort rule and last-good-temperature clause plus an llm check that every reference in the take_reading doc has its antecedent; the cooling comment's reason plus an llm check that the 700 °C claim never survives without it.
- 4 `cinder-delete-*` regexes (not_contains), plus the pointer-only `cinder-cite-src-pointer-gone`.
- Per shrink, 3 graders: cut part gone, kept part present, llm reading the survivor alone (`cinder-shrink-run-window-*`, `cinder-shrink-cone-*`).
- Citations: 0001/0003/0004 kept in `src/`; tests citation gone and claim kept; both architecture claims kept with their citation.
- 5 `cinder-term-*` regexes on declaration lines.
- 2 llm "nothing added" graders, for `src/controller.rs` and `src/schedule.rs`, with the original texts embedded.

Totals: 43 regex, 7 llm.

## Deliberately ungraded

- Whether "A temperature in quarter-degrees Celsius.", "Shortest on-time worth commanding.", "The kiln's rated maximum." or "A cone a preset can fire to" are trimmed: each is a near-restatement whose removal breaks nothing.
- Whether "Runs one control window." survives as a summary line.
- Comment reflowing and line wrapping; patterns accept `//`/`///` across line breaks.
- "Nothing added" in files other than controller.rs and schedule.rs (lower risk; their keeps are covered by regex).
- Whether the agent edits `docs/` or AGENTS.md (it should not need to; not checked).
