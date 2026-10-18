---
description: "Authoring. A task that adds behaviour over a device whose protocol holds one non-local fact: that fact reaches the code, nothing added only restates, domain words come from the lexicon, and new names say what things are or do."
tags: [code-style, authoring]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

We want the green weight to come straight off the bench scale instead of being typed in. Add a `roastlog/scale.py` that returns the scale's next stable weight in grams, and a function in `roastlog/log.py` that starts a new record: given the lot number it reads the green weight from the scale, stamps the charge time, and adds it to the log. No tests needed for this one; there's no scale in CI.
