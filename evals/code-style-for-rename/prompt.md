---
description: "code-style loads before a rename, where design-philosophy rightly does not: a name is how code reads."
tags: [code-style, trigger]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Rename `fetch_all` to `fetch_stations` everywhere it appears. Nothing else changes.
