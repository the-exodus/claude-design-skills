---
description: "A small fix: adversarial and design parity only; the repo's own out-of-scope policy overrides the default."
tags: [review-cycle, cycle, full]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 80
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
---

I've fixed the midnight departures bug on this branch. Run the review cycle before I open the PR.

The brief:

**Midnight departures are listed on two days**

A sailing that departs exactly at midnight is listed by `departures_on` for two days: the day it departs and the day before.

Acceptance criteria:
1. `departures_on(day)` lists a sailing departing at 00:00 on its own day, and not on the day before.
2. Nothing else about `departures_on` changes.
