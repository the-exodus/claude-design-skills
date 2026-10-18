---
# No surviving comment in controller.rs claims anything the original comments did not.
type: llm
focus: { source: file, path: src/controller.rs }
---
The only change asked for was tidying comments. Compare every comment now in `src/controller.rs` with the originals below. A comment may be kept, shortened, deleted, or reworded so that a shortened sentence still reads correctly (for example naming "the fault count" where a pronoun lost its antecedent). It must not gain new claims: no new facts, reasons, contracts, record citations or explanations that the originals did not state.

Original comments, in file order:
1. On `WINDOW`: "See 0002."
2. On `SystemClock::now`: "`Instant` stops while the Pi is suspended on Linux, so a suspend pauses the schedule instead of jumping it forward."
3. On `Firing`: "One firing of a schedule, from switch-on to the end of its last segment's soak."
4. In `Firing::new`: "`Schedule::new` rejects an empty schedule, so there is a first segment."
5. On `run_window`: "Runs one control window: reads the thermocouple, sets the relay for the window's duty and sleeps until the window ends. Call it again as soon as it returns: the relay is off between calls but the schedule's clock is not, so a slow caller leaves the kiln behind its schedule."
6. In `run_window`, on the soak timing: "Soak time is counted from when the kiln first reaches the target, not from when the ramp's planned time runs out, so a ramp the elements could not keep up with still gets its full soak."
7. In `run_window`, above the duty calculation: "The same duty calculation serves cooling segments. It keeps the relay off above about 700 °C, because the kiln sheds heat faster than any rate a schedule asks for, and fires the elements below that to slow the fall."
8. On `take_reading`: "Takes the next reading from the thermocouple and folds it into the fault count. Three in a row abort the firing (0003); a good reading resets it, and a fault short of the third reports the last good temperature instead."

PASS if every comment in the file can be traced to one of these, saying the same or less, and there is no comment on an item that had none (for example `PROPORTIONAL_BAND`, `Clock`, `Abort`, `Progress`, `setpoint`). Rewording that keeps the meaning is fine; so is adding a noun to repair a reference.
FAIL if any comment states something none of the originals stated: a new comment, a new reason or contract, a new or expanded citation (for example turning "See 0002." into a description of the window plus "(0002)"), or a description of behaviour the originals did not describe.
