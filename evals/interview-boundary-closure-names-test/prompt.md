---
description: "A branch closes by placing a new module and saying who may import it. The closure decides the architecture test that protects that boundary; the threshold branch closed beside it draws no boundary and gets no such test."
tags: [interview, boundary]
plugins: ["../../plugins/design"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

1. The second. The fetcher is where a socket error becomes data, nothing more. Silence gets a home of its own.
2. Your shape, one call: `gaugefeed/health.py`. `__main__` hands it the state it read, this cycle's outcomes and the cycle time, and gets back the per-station picture and the state to write. Only `__main__` imports health. `report` gets the picture as plain data and never imports it, and neither does `fetcher`. Health imports no other gaugefeed module. No third shape.
3. Facts. The file stores when each station last answered; health applies the rule when it builds the picture.
4. Wall time since the last reading. A host outage reading as silence is honest enough; telling "we stopped asking" apart is out of scope for now.
5. An hour. Nothing in between: the dashboard already greys a *stale* reading after two cycles, and that is the short-term hint.
6. Any reading resets it. Flapping gauges are out of scope; say so in the closure.
7. One threshold for every station.

Silent ends only when the station answers or someone takes it off the list. The rest is U7.

Recap U1 and U2 and close both. Then take U3.
