---
description: Consolidation of a sprawling glossary with planted defects (Stockroom, a warehouse service). Expected verdicts in expected.md.
tags: [lexicon, fixture]
plugins: ["../../plugins/design"]
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

This project's glossary has sprawled: it is past thirty entries, and a lot of them read like descriptions of the code rather than what the words mean. Please prune, consolidate and correct it.

I can't answer questions while you work, so take my sign-off as given and write the consolidated glossary in place, where it is now. It is the only file you change; everything else in the project is read-only. Anything that needs a decision from me, list it rather than settling it.

Put the full report in your final reply: a verdict for every entry with a one-line reason, where the content you cut already lives, anything you cut that has no other home, every place the glossary disagrees with the code or the docs with `file:line` evidence, references outside the glossary to words you retired, and any gaps you propose.
