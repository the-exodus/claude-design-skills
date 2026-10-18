---
type: llm
focus: { source: file, path: output.md }
---
The only change asked for was tidying comments. Compare every comment now in `src/schedule.rs` with the originals below. A comment may be kept, shortened, deleted, or reworded so that a shortened sentence still reads correctly. It must not gain new claims: no new facts, reasons, contracts, record citations or explanations that the originals did not state.

Original comments, in file order:
1. On `KILN_LIMIT`: "The kiln's rated maximum. The elements are rated higher, but the lid brick is not."
2. On `Segment`: "One ramp-and-soak step of a schedule."
3. On `Segment::rate_per_hour`: "Quarter-degrees per hour. Positive heats and negative cools; never zero, and the sign must agree with the direction from the previous segment's target to this one's. `Schedule::new` checks both."
4. On `Schedule::new`: "Checks a schedule once, at load, so that the controller can follow it without re-checking anything (0004)."
5. On `Schedule::segments`: "Returns the schedule's segments."
6. On `Schedule::planned_duration`: "Planned duration of the heating segments, ramps plus soaks, for a kiln starting at `from`. The display's end-time estimate is built on it."
7. On `Cone`: "A cone a preset can fire to: 06, 04, 5, 6 or 10. Cones are an enum rather than plain numbers so that a preset cannot name a cone with no known peak: `peak` matches every variant, so a cone added without its temperature fails to compile."
8. On `Cone::peak`: "Peak temperature at a 60 °C/h final ramp, from the cone maker's chart."

PASS if every comment in the file can be traced to one of these, saying the same or less, and there is no comment on an item that had none (for example `MAX_SEGMENTS`, `ScheduleError`, `Schedule`, `preset`, or a field other than `rate_per_hour`). Rewording that keeps the meaning is fine.
FAIL if any comment states something none of the originals stated: a new comment, a new reason or contract, a new citation, or a description of behaviour the originals did not describe (for example listing what `Schedule::new` rejects, or the cone numbers in a new form).
