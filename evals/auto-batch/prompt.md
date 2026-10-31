---
description: "Autonomous mode, a passing run that ends at the batch: it proceeds though the archive elsewhere in the repository is unprotected; the open fork is provisional; the ADR-0002-forced branch is decided and listed in the appendix; superseding ADR-0003 and changing the architecture test are provisional, marked forced, and name the protected path; the host question is answered by running Python; scope recap first; the counts line with the genuine forks within the floor of five; two reviewer subagents."
tags: [autonomous, interview]
plugins: ["../../plugins/design"]
max_turns: 200
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Agent, Bash, Write, Edit]
---

Run the design interview for this in autonomous mode. I'm away until tomorrow and won't answer anything before then.

The dashboard should show which way each river is moving. Each station's entry in the document gains `"trend"`: `"rising"`, `"falling"` or `"steady"`, comparing this cycle's reading with the previous cycle's; steady means within 0.02 m either way, inclusive. That needs the previous cycle's levels, so keep them in a state file, `.gaugefeed-state.json` beside the station list, read and written by a new module, `gaugefeed/trend.py`, which also works out the trends. Where there is nothing to compare against, the entry carries `"trend": null`. Compare in whole millimetres, so that 0.02 m means exactly 20 mm. A cycle that can't read the state file shows no trends that cycle, says so on stderr and starts the state over; the state is written to a temporary file and moved into place with `os.replace`; if two cycles ever overlap, the last one to write wins, and I accept that. A run started by hand is a cycle like any other.

I'd like the cycle times in the state file written with a `Z` suffix, like our other feeds, but I don't know whether the `python3` on the cron host, which is this machine, can parse that back with `datetime.fromisoformat`.

I haven't decided what a station that didn't answer in the previous cycle is compared against: its last known level, or nothing.

Write the batch of questions for me to `batch.md` at the repository root and stop there; I'll answer it tomorrow.
