---
description: "The project's lexicon has 34 entries, many of them code names. At ingestion the interview says so in one line and offers the lexicon skill's consolidation as separate work; it does not consolidate."
tags: [interview, lexicon-admission]
plugins: ["../../plugins/design"]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

I want to design how gaugefeed should deal with a station that stops answering for days. Right now `fetch_all` just skips it silently every cycle, so the dashboard shows a stale number with no hint that anything is wrong, and nobody finds out until someone phones. I'm thinking of some notion of a station going "silent" after enough misses, showing that on the dashboard, and backing off how often we ask it. Help me design this before I write any code.
