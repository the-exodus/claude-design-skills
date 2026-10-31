## `U1` — Where the silence knowledge lives · **decided**

Silence is its own concern in `gaugefeed/health.py`, behind one call: `__main__` hands it the state it read, this cycle's per-station outcomes and the cycle time; it returns the per-station picture for the report and the state to write. Health imports no gaugefeed module and reads neither clock nor disk — the cycle time comes in as an argument, the same way ADR-0002 keeps the report honest. The state file holds facts — when each station last answered — and health applies the rule when it builds the picture, so the stored data outlives any change to the threshold. Only `__main__` imports health; `report` gets the picture as plain data. `tests/test_architecture.py` declares `gaugefeed.health` with no gaugefeed imports and adds it to `__main__`'s list only, so `report` or `fetcher` importing it fails the test, citing the new ADR.

ADR-0001 is read narrowly: the fetcher is where a socket error becomes data, and nothing more. **Fork:** rejected putting silence behind the fetcher, because it would give the one network module a clock and a disk and make every test of the threshold patch the network; rejected `__main__` doing the comparison itself, because the concept would exist only in a script that nothing tests.

## `U2` — When a station counts as gone silent · **decided**

A station is silent when an hour has passed since it last answered, measured in wall time from the stored timestamp, not in consecutive failed cycles. One threshold for every station. Any reading clears it. Nothing sits between answering and silent: for the first hour the dashboard's own greying of a *stale* reading after two cycles is the short-term hint. Silence ends only when the station answers or someone takes it off the list; the decommissioned-but-still-listed case is `U7`.

**Fork:** rejected counting consecutive failed cycles, because a host outage would read as every station missing one cycle rather than as nobody having been asked for a day; telling "we stopped asking" apart from "the station stopped answering" is **out-of-scope for now**. Rejected a middle state, on the grounds above. Flapping gauges are **out-of-scope**: a gauge answering one cycle in fifty never trips the rule, and that is accepted.

Worth noting the wall-time choice behaves better than I framed it in the probe: after a three-day host outage, every station has a three-day-old timestamp, but the ones that answer on the first cycle back update it immediately and never appear silent. Only the genuinely dead ones surface.

## Adversarial check

One thing I found in the code that bites `U2`'s "any reading resets it". `fetch_reading` calls `json.loads`, which raises `JSONDecodeError` — a `ValueError`, not an `OSError`. `fetch_all` catches `OSError` only (`fetcher.py:22`), so a station that answers HTTP 200 with malformed JSON doesn't get skipped: it propagates out of `fetch_all` and kills the cycle. Today that silently costs the whole document; under this design it also means one station can stop every other station's timestamp from being updated, and a cycle that crashes writes no state at all. "Any reading resets it" presumes we agree what a reading is, and right now a garbage payload is neither a reading nor a failure.

Does a station that answers with garbage count as answering? `T1` owns the full question, but `U2`'s closure needs the one-line answer, so I'd rather amend it now than reopen it later.

Second, smaller: does the document say "silent since T", and if so is T the last answered time or the moment the threshold was crossed? I'd recommend the document carry the plain fact — last answered at T — and let the dashboard write the sentence. It dodges the ambiguity, it's the fact an operator actually wants ("we haven't heard from it since 10:00"), and it keeps the report free of the rule. `D2` owns it; flagging it here because it's the one place the facts-only choice could still leak a judgement into the document.

## Lexicon

**Admitted: `silent`.** Closing `U2` required the word to carry a fixed boundary, and it has to be kept from colliding with the inherited `stale`:

> **silent** — Said of a *station* that has not answered for an hour. It stops being silent as soon as it answers. Distinct from *stale*, which is the age of a *reading* the dashboard already holds: a silent station's last reading also goes stale, but a stale reading does not mean the station is silent.

`stale` is inherited and untouched — this design didn't change what it means. Six entries now, one new.

**Refused:** *picture* and *outcome*, the values health takes and returns, and *health* itself. They're this design's structure, not the domain's language — they belong in the code and the tree. If the document ends up with a field the dashboard's users read, that word may earn an entry later.

## What closing these changed

- `U6` got sharper and is now load-bearing: facts-only storage means a station that has **never** answered has no timestamp, so the rule has nothing to subtract from. First run and newly-added stations hit this on cycle one.
- `P3` has a real tension to resolve. If `__main__` reads *and parses* the file and hands health dicts, the format is known in two modules and changing it edits both — the read/compute/write split from "don't decompose by time". If `__main__` hands over bytes and health owns the parse, there's one owner. Not a contradiction with `U1`, so I'm not reopening it; `S1` and `P3` take it together.
- `E1` gains a concrete item: `health` needs an `ALLOWED` entry in `tests/test_architecture.py` and `__main__`'s allow-list grows a fourth module.
- New branch seeded, `U8`: a cycle that crashes partway writes no state, so every station's timestamp stands still while the clock doesn't. Interacts with the JSON finding above and with `U4`.

**ADR-worthy:** `U1`, as a *partial* supersede of ADR-0003 — that ADR records two decisions, and only the "keeps no state" half is being overturned; cron-and-fresh-process and the daemon rejection still stand, so ADR-0003 keeps its status with a partly-superseded note. `U2`'s rule is ADR-worthy on its own (one decision per ADR). Both get written in Phase 9, not now.

---

## `U3` — Lifecycle: how silence begins, persists, and ends

Open because `U1` made most of the lifecycle *derived* rather than stored — with only a last-answered timestamp on disk, there is no recorded moment of transition. That's clean, and it quietly forecloses some things. This is a fork: transitions derived, or transitions recorded.

1. Does anything need to know that *this cycle* is the one where a station crossed into silence? Nothing on disk can tell you — last-answered doesn't change at the crossing, so every cycle after the hour looks identical. That's the difference between a dashboard that shows a state and anything that could ever fire once on the transition (`U5`).
2. When a station comes back after two days out, does the document say anything about it having been silent, or does it simply reappear as a normal station? Under facts-only, the second is free and the first needs storage.
3. Does the state file carry a row for every station on the list, updated every cycle, or only rows for stations that have ever answered? That decides whether the file is a mirror of `stations.txt` or a sparse log of successes — and it's the same question `U6` asks from the other end.
4. Does a currently-answering station's row hold anything besides the timestamp? Asking because every field we add is a fact the next threshold change has to stay compatible with.
5. What else could this be? The alternative worth naming: store `first_failed_at` alongside `last_answered`, cleared on any success. It makes "silent since" exact, survives a threshold change, and makes the transition detectable — at the cost of a second field that can disagree with the first, and a rule about which wins. Is the transition worth that, or is derived-only right for what the dashboard needs?
