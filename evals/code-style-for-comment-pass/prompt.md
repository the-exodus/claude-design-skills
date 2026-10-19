---
description: "code-style loads before a pass over comments that changes no behaviour."
tags: [code-style, trigger]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Tidy up the docstrings in `gaugefeed/fetcher.py`. Leave the code itself alone.
