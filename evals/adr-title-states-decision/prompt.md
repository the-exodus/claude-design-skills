---
description: "Asked by topic to record a decision, the ADR's title states what was decided, not the topic."
tags: [adr]
plugins: ["../../plugins/design"]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Can you record our decision about retries? We settled it today. When a gauge doesn't answer, we retry three times with a doubling delay starting at two seconds, then mark the station silent and move on, rather than keep hammering it. We looked at retrying forever with a capped delay, but a dead gauge would hold a worker for good.
