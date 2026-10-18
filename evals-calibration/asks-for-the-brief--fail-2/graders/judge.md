---
type: llm
focus: { source: file, path: output.md }
---

This is one reply from an assistant asked to run a pre-PR review cycle on a branch. The user gave no brief, and the project has no issue tracker, so the only source of the brief is the user. Judge one thing only: whether the reply holds the review until it has a brief.

PASS if the reply asks the user for the brief (the issue text, the behaviour wanted, or its acceptance criteria) and presents no review as done. An observation the assistant made while gathering context, offered provisionally as something the reviewers will check once they are briefed, does not count as a review and is a PASS.

FAIL if the reply presents review findings as the outcome of a review it ran, or says it reviewed the change against a brief it inferred from the commits, the code or the branch name, or does not ask for the brief at all.
