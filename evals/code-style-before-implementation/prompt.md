---
description: "code-style and design-philosophy both load before the first edit of an implementation request that adds behaviour and names neither."
tags: [code-style, trigger]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add retry with backoff to the fetcher. Stations drop the odd request and right now one hiccup loses that station's reading for the cycle.
