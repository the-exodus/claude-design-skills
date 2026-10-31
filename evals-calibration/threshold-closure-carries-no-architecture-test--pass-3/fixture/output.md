## `U1` recap — where the silence knowledge lives

A new module `gaugefeed/health.py` owns the silence concept. One call: `__main__` hands it the prior state, this cycle's per-station outcomes and the cycle time; it returns the per-station picture for the document and the state to write. The file stores facts — when each station last answered — and health applies the rule when it builds the picture, so a change to the threshold reinterprets stored data rather than invalidating it. Only `__main__` imports health; health imports no gaugefeed module; `report` and `fetcher` never see it. ADR-0001 is read narrowly: the fetcher is where a socket error becomes data, not where failure is judged.

Interface check (`P1`, `P3`): health hides the threshold, the date arithmetic and the file format behind one call, and the caller needs to know none of them — that's a deep module behind a small surface. Rejected alternative: `__main__` comparing timestamps itself, which is shorter today and puts the only copy of the rule in an unimportable script.

## `U2` recap — when a station counts as gone silent

A station is silent when more than an hour of wall time has passed since its last reading, measured against the cycle time. Not consecutive failed cycles: a host outage then reads as the stations having gone quiet, which is accepted as the honest-enough lie, and distinguishing "we stopped asking" is out of scope for now. Any reading clears it outright — no decay, no counter — so a flapping gauge that answers once an hour never trips, accepted because outages here are long and continuous. One threshold for every station. Nothing exists between answering and silent: for the first hour the dashboard's own `stale` greying is the short-term hint. Silence ends only when the station answers or the station leaves the list (`U7`).

"More than an hour" is exclusive. At five-minute cycles nothing lands on the boundary except by coincidence, so I'm recording the wording as the decision rather than making it a question.

## Lexicon

One admission, against the three tests: **silent** — said of a *station* that has not answered for more than an hour. Distinct from *stale*, which is said of a *reading*'s age and is the dashboard's own; a station can be silent while the dashboard still shows its last reading, greyed.

It passes on the strongest ground available: it names a distinction that must not be conflated, which is exactly what you insisted on in your answer. Refused in the same breath: *health* (a module, test 1), the *picture* (a hand-off between two components, test 1), *state file* (a file, test 1), *last answered* (ordinary sense, test 2). Six entries now, all but one inherited.

One flag: if `T1` decides that a station answering with garbage doesn't count as answering, this entry's "has not answered" changes meaning and the entry is amended then.

## Adversarial check

Two things, and the first one I don't think closes.

**The rule has no answer for a station with no last reading.** Wall time since the last reading requires a last reading. A gauge added to `stations.txt` that has never once answered has no fact in the file, so health cannot compute a duration for it — and that is your pitch's own worst case surviving the fix: someone adds a gauge, it never works, the document carries no entry, the dashboard shows nothing with no hint why, and the phone rings. The *policy* for new stations is `U6`, but `U2`'s rule has to say what an absent record means before `U6` can have an opinion, and `C4`'s data shape depends on the answer. Does the file carry a second fact per station — when gaugefeed first asked about it — so a never-answering station accrues silence from first sight? Or does the picture carry a third state, never-answered, distinct from silent?

**Format ownership is split between two modules.** You said `__main__` hands health "the state it read". If `__main__` does the `json.load`, then `__main__` knows the file is JSON and knows its top-level shape, and health knows the record shape — so changing the format edits both, which is decomposition by time and the wrong answer to `P3`. The alternative is the symmetry you already have in ADR-0002: `report` returns a JSON string and `__main__` prints it, so health takes the state as *text* and returns the next state as *text*, with the format wholly in health and the I/O wholly in `__main__`. Third option, health opens the file itself — no ADR forbids it, since ADR-0001 only governs the network, but health then stops being testable with plain values the way report is.

Which of those, and which shape for the never-answered case? Separately and for the record, a clock stepping backwards puts a last-answered time in the future, which reads as recently answered and so fails toward not-silent — the safe direction. I'm noting it under `S4` rather than holding this branch for it.
