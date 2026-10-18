---
description: "A change of records only: design parity in records-only mode, no suite, and the brief checked against itself."
tags: [review-cycle, cycle, full]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
---

This branch records the refund rule as an ADR. Run the review cycle before I open the PR.

The brief:

**Record the refund rule**

Why: staff at the ticket office compute refunds by hand and disagree about rounding.

Behaviour: record, as an ADR, how the refund for a cancellation within the cancellation window is computed and paid.

Acceptance criteria:
1. An ADR records the refund rule and the alternative that was rejected.
2. The ADR index lists it.
3. The rule is consistent with criterion 5.

Edge cases: a cancellation outside the refund window gets no refund.
