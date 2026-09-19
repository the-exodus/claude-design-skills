---
description: "A branch closes by introducing a new module and class. Their names are the design's structure and are never admitted to the lexicon."
tags: [interview, lexicon-admission]
plugins: ["../../plugins/design"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

No distinction meant by "usable"; "no reading" is right.

1. Every station in the *station list* appears in the output every cycle, whatever happened to it.
2. The state, since when, and when it was last asked. The rest goes to the log.
3. Fetching owns it. One new module, `gaugefeed/health.py`, with a `StationHealth` class that reads the state file, decides which stations to ask this cycle, and writes it back. `fetch_all` calls it, and nothing else knows the state machine.
4. The dashboard deploys first. It ignores fields it doesn't know.
5. The sibling block: keep `{url: reading}` exactly as it is and add a `health` block beside it. Nothing to add to your two.

Recap and close. Then take the dashboard representation branch, against *stale*, next.
