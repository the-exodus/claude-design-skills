---
# The reply asks for the brief.
type: llm
focus: last_message
---

The user asked for a review cycle on a branch but gave no brief, and the project has no issue tracker.
PASS if the reply asks the user for the brief (the issue text, the behaviour wanted, or its acceptance criteria) before any review is done.
FAIL if the reply presents review findings, or says it reviewed the change against a brief it inferred from the commits, the code or the branch name, without asking.
