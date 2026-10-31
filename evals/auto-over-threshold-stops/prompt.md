---
description: "Autonomous mode, decision D as amended: a feature whose genuine forks exceed a third of the decided branches and the floor of five. The run stops, recommends a live interview, hands over the tree so far with its counts line where the batch would have gone, and writes no brief."
tags: [autonomous, interview]
plugins: ["../../plugins/design"]
max_turns: 150
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Agent, Bash, Write, Edit]
---

Run the design interview for this in autonomous mode. I'm away until tomorrow and won't answer anything before then.

The dashboard should show each station the way the people reading it think of it, not as a URL: a name, the river it is on, the level at which the dashboard should turn it red, and the unit to show its levels in, metres or feet, with the stations grouped by river. Gaugefeed has to carry all of that in its document. Stations stay identified by their URL and keep reporting `level_m` in metres, so the fetcher and what it hands back don't change. Beyond that I haven't decided anything about it yet: where the settings live or what they look like, what a station with no settings shows, whether gaugefeed or the dashboard converts the units, how the document changes, how the grouping and the order work, whether a station can sit in more than one group, whether a station that doesn't answer still appears under its river, what turning red means exactly, whether there is an amber level below red, whether a station can be hidden without taking it off the list, how a station keeps its settings when its URL changes, and how many decimals the levels are shown with.

Write the batch of questions for me to `batch.md` at the repository root and stop there; I'll answer it when I'm back. Once I have, the brief goes in `docs/briefs/station-display.md`.
