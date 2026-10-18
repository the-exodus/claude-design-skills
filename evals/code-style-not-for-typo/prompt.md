---
description: "code-style does not load for a typo fix in prose, which writes no code, name or comment."
tags: [code-style, trigger]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

There's a typo in the README: it says "guage". Fix it.
