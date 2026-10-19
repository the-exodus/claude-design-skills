---
type: llm
focus: { source: file, path: output.md }
---

This is a Java interface after an assistant was asked to tidy a project's comments. Judge one comment only: the Javadoc on `onDoorLatched(CompartmentId id, Instant at)`. Before the tidy it read:

> The door has latched and the sensor's debounce has run: the bank starts the dwell clock from this moment, not from the courier's scan. Called on the lock-board thread.

The right change cuts "The door has latched and", which the method's name says, and keeps the contract: the call comes once the sensor's debounce has run, the bank starts the dwell clock from it rather than from the courier's scan, and it is called on the lock-board thread.

Read the comment as it is now, on its own, as a reader who has not seen the original would.

PASS if the comment is still there, reads as complete sentences with nothing whose referent was cut, keeps the three parts of the contract (after the debounce, the dwell clock from this moment not from the scan, the lock-board thread), and claims nothing the original did not. Whether the opening clause was cut is judged elsewhere; a comment left whole passes this check.

FAIL if the comment is gone, if any of the three parts of the contract is lost, if it now says something false or wider than the original (for example that the dwell clock starts at the scan, or that the call comes on the bank's executor), or if it adds a claim. Quote the comment as it is now in your reasoning.
