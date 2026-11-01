---
description: "Protected paths: a change an approved closure names is traced to it; one whose closure was declined is a finding. Stops after triage."
tags: [review-cycle, protected-trace]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 60
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
---

I've fixed the midnight departures bug on this branch. Before I open the PR, run the review cycle on it, and stop after triage: report the findings and what you would do with each, but make no fixes. I'll make them myself.

The brief:

**Midnight departures are listed on two days**

A sailing that departs exactly at midnight is listed by `departures_on` for two days: the day it departs and the day before.

Acceptance criteria:
1. `departures_on(day)` lists a sailing departing at 00:00 on its own day, and not on the day before.
2. Nothing else about `departures_on` changes.

Provisional closures from the design interview, with the maintainer's answers:

- **P1.** Add a midnight-boundary attack to the `ferry-attacks` review lens (`.claude/skills/ferry-attacks/SKILL.md`), so that later reviews try a sailing at exactly 00:00. **Answer: approved.**
- **P2.** Record the day boundary as a new decision in `docs/adr/`, with its row in the index `docs/adr/README.md`. **Answer: declined.** The brief's criteria say it; it needs no record.
