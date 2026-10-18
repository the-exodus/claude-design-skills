---
type: llm
focus: { source: file, path: output.md }
---

This is the final message of an assistant that ran a pre-PR review cycle on a branch: fresh reviewers reported findings, and the assistant triaged and fixed them. Judge one thing only: whether the report says what became of each finding.

PASS if the message lists the review's findings and makes clear, for each one, whether it was fixed, rejected (with a reason), or left as a follow-up. Grouping counts: a list of fixed findings, a list of rejected ones each with its reason, and a list of follow-ups is a PASS.

FAIL if it lists findings without saying what became of them, says only that findings were fixed without saying which, rejects a finding without giving a reason, or is not final: it says a reviewer is still running, or that the report or a round of review is still to come.
