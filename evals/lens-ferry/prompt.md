---
description: "The lenses on the seat-holds branch: each planted defect caught, each trap not flagged. Stops after triage."
tags: [review-cycle, lens, lens-ferry]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 60
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
---

Before I open the PR for this branch, run the review cycle on it, and stop after triage: report the findings and what you would do with each, but make no fixes. I'll make them myself.

The brief:

**Seat holds**

Why: passengers at the ticket office lose a space while they fetch a card, because a booking is only made once they pay. A hold keeps the space for a few minutes.

Behaviour: making a booking places a hold on the space for `hold_minutes` (15 by default, set in `defaults.json`). `confirm(ref)` turns a hold into a confirmed booking. A hold that is not confirmed in time lapses and its space is released; the first passenger on that sailing's waitlist then gets a hold of their own. Holding a space costs a fee of a tenth of the fare, credited on confirmation.

Acceptance criteria:
1. A hold lasts `hold_minutes`, as set in `defaults.json`.
2. A hold that has lapsed cannot be confirmed: `confirm` raises `HoldExpired`.
3. When a hold lapses or is cancelled, its space is released and the first passenger on the sailing's waitlist gets a hold.
4. A passenger has at most one hold per sailing: placing a second replaces the first.
5. Holds survive a restart of the booking service: `save_holds` before stopping, `load_holds` after starting.
6. The hold fee is a tenth of the fare, in øre.

Edge cases: a hold on a sailing with no free space raises `FullError`; reserved car spaces are never held.
