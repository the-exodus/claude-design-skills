---
# The surviving doc comment on HELD_FOR_INSPECTION stands on its own and is true.
type: llm
focus: { source: file, path: src/lockerline/StatusCodes.java }
---

This is a Java class of status constants after an assistant was asked to tidy a project's comments. Judge one comment only: the Javadoc on `HELD_FOR_INSPECTION = 7`. Before the tidy it read:

> The status of a compartment customs is holding: distinct from 0 (empty), 1 (occupied), 2 (awaiting collection) and 5 (fault), so that the courier app can tell an inspection from a fault and does not send an engineer.

The right change keeps the purpose: the code is distinct from the other statuses, so that the courier app can tell an inspection from a fault and does not send an engineer. It drops the re-listing of the other codes, which duplicates the constants defined just above and is the half that goes stale when a status is added.

Read the comment as it is now, on its own, as a reader who has not seen the original would.

PASS if the comment is still there, still says that the code is distinct from the other statuses (in any words) and why (so the courier app can tell an inspection from a fault, or does not send an engineer), reads as complete sentences, and claims nothing the original did not. Whether the list was dropped is judged elsewhere; a comment left whole passes this check.

FAIL if the comment is gone, if it no longer says why the code must be distinct, if "distinct" survives with nothing left to be distinct from, or if it adds a claim (a new status, a reason the original did not give). Quote the comment as it is now in your reasoning.
