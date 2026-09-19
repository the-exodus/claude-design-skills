---
description: "A new ADR takes the next number after the highest, not the gap, in the house format, and the index gains its row in the same change."
tags: [adr]
plugins: ["../../plugins/design"]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

We've decided to keep every timestamp in UTC end to end and convert to the station's local time only when rendering. Two of our stations sit either side of a daylight-saving boundary, and last month's spring-forward put a duplicate hour in the pilots' chart. The alternative we looked at was storing local time with an offset column; we rejected it because every query that compares stations would have to normalise first.

Please write that up for the record. Use exactly this title: Keep timestamps in UTC and convert only when rendering
