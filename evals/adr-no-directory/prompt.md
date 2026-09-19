---
description: "Where the repo has no ADR directory, the skill asks where, with a concrete suggestion, and creates nothing."
tags: [adr]
plugins: ["../../plugins/design"]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

We've decided to keep every timestamp in UTC end to end and convert to the station's local time only when rendering, because two stations sit either side of a daylight-saving boundary and spring-forward put a duplicate hour in the pilots' chart. Storing local time with an offset column was rejected: every cross-station query would have to normalise first.

Please write that up as an ADR.
