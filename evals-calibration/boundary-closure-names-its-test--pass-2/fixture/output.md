## `U1` Where the silence knowledge lives — **decided**

A new module, `gaugefeed/health.py`, owns the notion of silence. ADR-0001 means only that the fetcher is where a socket error stops being an exception and becomes data; it does not make the fetcher the owner of judgements about a station over time. Health is a pure function of its arguments: `__main__` hands it the state it read, this cycle's per-station outcomes and the cycle time, and gets back the per-station picture and the state to write. Health imports no other gaugefeed module and does no I/O — no clock, no disk. Only `__main__` imports it; `report` receives the picture as plain data, which is what ADR-0002's consequences already required of any feature needing more than readings.

**To confirm:** I'd have `tests/test_architecture.py` declare `gaugefeed.health` with no gaugefeed imports and add it to `__main__`'s allowed list only, so `report` or `fetcher` importing health fails the test, with the entry citing the new ADR. Is that the boundary you meant?

The state file stores **facts** — when each station last answered — and health applies the rule when it builds the picture.

**Fork.** Rejected: silence behind the fetcher, because it gives the fetcher a clock and a disk and conflates "this socket failed" with "this station has stopped answering" — two concerns with different test setups and different reasons to change. Rejected: `__main__` doing the comparison itself, shorter today but it puts the only copy of the concept inside a script, where it can't be tested. Rejected: storing the judgement ("silent since T") rather than the fact, because that cooks the threshold into the history — change the hour and nothing already written reinterprets.

**Adversarial check, one finding that doesn't reopen this.** Health being pure means `__main__` now holds the file path, the read, the write — and if `__main__` parses the file into a dict before handing it over, then the state *format* has two owners: `__main__` owns bytes-to-dict and health owns dict-to-meaning. That's the pipeline smell. The alternative is that health takes and returns the serialized form and `__main__` only moves bytes. I'm not deciding it here because it can't close before the format does; it is now the concrete question `P3` and `S1` have to answer together, and the module boundary above holds either way.

## `U2` When a station counts as gone silent — **decided**

A station is silent when more than an hour has passed since it last answered. Measured as wall time since the last reading, not as consecutive failed cycles. One threshold for every station. Any reading resets it. Nothing sits between answering and silent: the dashboard's own `stale` greying, at two cycles, is the short-term hint, and the silence threshold is twelve cycles out from there.

**Fork.** Rejected: counting consecutive failed cycles, because it diverges from wall time exactly when the host has been down — a cycle count would say every station missed one cycle when in fact nobody asked for a day. Rejected: per-station thresholds, because the station list is one URL per line with nowhere to put a second field, and no station needs a different number today.

**One correction to my own framing.** I put wall time to you as choosing which lie to prefer. It's better than that, because the picture is built *after* the fetch: a cycle following a day of host downtime fetches, the stations answer, last-answered becomes now, and nobody is silent. A host outage on its own produces no false silence. What survives is narrower — for a station that is genuinely dead, the reported duration includes time we weren't asking, and the document can't tell the two apart. That's the piece you put out of scope.

**Sub-branch, `U2a` — distinguishing "the station stopped answering" from "we stopped asking": deferred-later.** Reason: not needed while cron is reliable. What would bring it back: evidence of a host outage long enough that an operator misreads a silence duration, or anything that starts consuming the duration as a number rather than reading it.

Flapping gauges are explicitly out of scope: a station that answers one cycle in fifty resets on every answer and never trips.

**Lexicon.** Two terms admitted, both required by these closures:

- **silent** — said of a *station* that has not answered for longer than the *silence threshold*. About the station's answering, not about any *reading*'s age; a *stale* reading is the dashboard's separate notion.
- **silence threshold** — the time since a *station* last answered beyond which it counts as *silent*. One hour, the same for every station, measured as wall time and not in *cycles*.

Refused: `health`, the name of a component this design introduces. Refused: "picture" — the shape of the data handed to the report is this design's structure, not the domain's vocabulary; if the document needs a word for it, `D2` is where that gets earned.

## Tree changes from these closures

One branch added: **`S5` where the state file lives and how the process learns the path** — `/var/lib/gaugefeed` is yours, but `__main__` currently takes exactly one argument, and a second path changes the cron line and therefore the operator's install. `P3` is sharpened as above. `E1` now has a concrete item: `gaugefeed.health` needs an `ALLOWED` entry and `__main__`'s set grows by one.

---

## `U3` Lifecycle — how silence begins, persists, and ends

Open because the state and the threshold now fix when silence *starts*, and say nothing about the transitions around it. Your "silent ends only when the station answers or someone takes it off the list" closes the end condition; what the system *does* at each transition is still open, and the recovery edge is where I expect the disagreement.

1. When a silent station answers again, does anything say so? Right now the station's entry simply stops being silent and the document looks like it always did. The complaint in your pitch is that a station going quiet is invisible until someone phones — the mirror of that is that a station coming back is equally invisible, and the operator who finally drove out to the gauge has no way to confirm from the dashboard that the fix took. Does recovery need to be visible, and if so is that the document's job or the log's?

2. Does the state carry anything per station besides last-answered? A "silent since" is just last-answered under a different name, so I'd say no — but the facts decision does rule out recording things like "first noticed silent at", which is the field a recovery notice would otherwise want. Confirm I'm not throwing away something you'll need.

3. What updates last-answered — a fetch that returned without raising, or a fetch that returned a usable reading? These come apart when a gauge's web server answers 200 with junk, or with a payload that has no level in it. Under the first rule such a station is never silent, and your dashboard shows a station that is answering and useless. (`T1` owns what counts as garbage; I need to know whether the lifecycle hangs off "answered" or "gave us a reading", because the two produce different systems.)

4. Does a silent station's document entry still carry the last reading gaugefeed had, or only the silence? The dashboard keeps its own last reading and greys it, so carrying the reading again may be redundant — but then gaugefeed's document alone can't tell you what the river was doing when the gauge stopped, and the two repos disagree about who remembers.

5. Is silence per station only, or does the design need a notion of the fleet being silent? Three stations behind one network path go silent together, and twelve entries saying "silent" is an operator's problem, not a station's. Out of scope is a fine answer; I want it said, because if the answer is ever yes it changes what health returns.
