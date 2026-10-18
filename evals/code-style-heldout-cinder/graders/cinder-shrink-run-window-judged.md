---
# The surviving run_window doc stands on its own and is true.
type: llm
focus: { source: file, path: src/controller.rs }
---
Find the doc comment on `Firing::run_window`. The original read:

> Runs one control window: reads the thermocouple, sets the relay for the window's duty and sleeps until the window ends. Call it again as soon as it returns: the relay is off between calls but the schedule's clock is not, so a slow caller leaves the kiln behind its schedule.

The first sentence narrates the body, which is in view; the second is a caller contract that lives nowhere else. A correct result keeps the contract and drops the narration (a short summary such as "Runs one control window." may remain).

PASS if the surviving comment contains the contract (call again as soon as it returns; the relay is off between calls while the schedule's clock keeps running; a slow caller leaves the kiln behind), reads as complete sentences on its own with nothing referring to text that was cut, and says nothing false about the code (after the call returns the relay is off, and the setpoint is computed from elapsed clock time).
FAIL if the contract is missing or weakened, if a surviving sentence depends on the cut text to make sense, or if the comment now claims something the code does not do.
