---
# D1: postpone changes the blast before its checks, so a refused postpone leaves the blast moved and the counter spent.
type: llm
focus: last_message
---

In the branch, Schedule.postpone assigns the new time and increments the postponement counter before the rule and notice checks run, so a postpone that is refused still leaves the blast at the refused time with an allowance used.
PASS if the report states this defect: a refused or failed postpone leaves the blast's state changed (its time or its postponement count), because it mutates before validating.
FAIL if it does not report it.
