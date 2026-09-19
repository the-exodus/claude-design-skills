---
description: Held-out. Consolidation of a lexicon with planted defects (Tessera, a tiling window manager). Expected verdicts in expected.md. Never edit the skill in response to a failure here.
tags: [lexicon, fixture, held-out]
plugins: ["../../plugins/design"]
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

This project's lexicon has sprawled: a lot of its entries read like descriptions of the code rather than what the words mean. Please prune, consolidate and correct it.

I can't answer questions while you work, so take my sign-off as given and write the consolidated lexicon in place, where it is now. It is the only file you change; everything else in the project is read-only. Anything that needs a decision from me, list it rather than settling it.

Put the full report in your final reply: a verdict for every entry with a one-line reason, where the content you cut already lives, anything you cut that has no other home, every place the lexicon disagrees with the code or the docs with `file:line` evidence, references outside the lexicon to words you retired, and any gaps you propose.
