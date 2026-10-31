---
description: "A decision that draws a boundary, with an architecture test landing beside it, is recorded with the sentence that says the boundary is enforced."
tags: [adr, boundary]
plugins: ["../../plugins/design"]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

We've decided that the flood page gets its levels only through the `readings` module and never opens a station's SQLite file itself. Last week a change to the flood page's query read a station file while the poller was migrating its schema, and the page showed blanks for an hour. The alternative was to let the flood page query the station files directly, which is what it did; we rejected it because every page that does that has to know the one-file-per-station layout and keep up with each file's schema. I've added a rule to our architecture tests that fails if anything under `tidewatch/flood/` imports `sqlite3`; it goes in with this change.

Please write that up for the record. Use exactly this title: The flood page reads levels only through the readings module
