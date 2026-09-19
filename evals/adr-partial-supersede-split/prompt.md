---
description: "One of two decisions in an ADR changes: the ADR is split inside the supersede, as in the skill's worked example, and its status names both successors."
tags: [adr]
plugins: ["../../plugins/design"]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

The backup half of ADR-0001 has changed. The disk failure in March cost us most of a day of readings at two stations, because the nightly copy was twenty hours old. We're replacing the nightly copy with continuous replication of each station's SQLite write-ahead log to object storage, so a failure loses seconds. The storage decision itself stands: one SQLite file per station.

Please record this properly.
