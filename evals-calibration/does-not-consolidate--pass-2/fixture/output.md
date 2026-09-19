Scanned the repo. It's small: `gaugefeed/fetcher.py` (two functions), an empty `__init__.py`, `stations.txt`, a README, and `docs/lexicon.md`.

**Prior art:** no ADRs anywhere, no assumptions record. `docs/lexicon.md` exists and is binding. It has 34 entries, which is past the useful size; consolidating it is separate work for the `design:lexicon` skill.

**One line I need from you:** which open questions on your tracker touch this work, if any?

## What I understand you're building

Gaugefeed gains a per-station notion of health that outlives a single cycle. A station that misses enough consecutive fetches is declared **silent**; the dashboard shows that state instead of quietly rendering the last number; and silent stations get asked less often until they answer again.

**Change type: mixed.** `fetch_reading` probably survives untouched. `fetch_all` changes shape — today it returns successes only and discards failures at `fetcher.py:23`, and a silent-station design needs the failures. And there's new state that exists nowhere in gaugefeed today.

**Blast radius:** `fetcher.py` (both functions), the readings-dict contract the dashboard reads, whatever runs the cycle loop, and possibly station identity in `stations.txt`.

## Four lexicon collisions, before anything grows on top of them

1. **`stale` is already taken, and it isn't what you mean.** The lexicon defines it as a reading older than two cycles — ten minutes — still shown, explicitly distinct from having no reading. You said "stale number" loosely. So `silent` and `stale` would coexist: stale is a ten-minute property of a *reading*, silent is a multi-day property of a *station*. If we don't nail that down the dashboard ends up with two overlapping badges.
2. **`outage` is defined as gaugefeed's own network failing.** That distinction exists in the vocabulary and nowhere in the code. If gaugefeed's link drops for a day, every station accrues misses and the whole list goes silent — an outage laundered into N station faults.
3. **`backfill` is defined — readings pulled from a station's own memory once it's reachable again — but no code implements it.** If it's real, coming back from silence is exactly when it fires, and that changes what recovery means.
4. **`metered link` — a connection billed per request.** That gives backoff a second motive beyond politeness, and it's per-station, which may mean backoff isn't one global curve.

## Assumptions I'm carrying (shoot these down now if they're wrong)

- **A1.** Misses leave no trace today — no log, no counter, nothing. *(Verified: bare `continue`.)*
- **A2.** The dashboard renders the last known reading indefinitely when a station is missing from the readings dict. *(Your words, but the dashboard isn't in this repo, so I can't check what it actually does with an absent key.)*
- **A3.** A missed fetch means the station's fault, not gaugefeed's.
- **A4.** "Days" means the design must survive gaugefeed restarts inside the silence window.
- **A5.** There's an operator to phone, and the design's job is to shorten the time to that call — not to replace it.

## Out of scope unless you say otherwise

Active notification (paging, email); backfill on recovery; the public flood page; alert/flood level logic. **A2 and the notification exclusion are my shakiest guesses** — "nobody finds out until someone phones" could mean the dashboard is enough, or it could mean the dashboard is not enough and you want something to reach out.

## Two things the code can't tell me

- **Where does cross-cycle state live?** `fetch_all` is stateless and pure. A miss counter has nowhere to go today. This is foundational — everything else hangs off it.
- **Who calls `fetch_all`, and where does the dashboard get its data?** The README says `python -m gaugefeed stations.txt`, but there's no `__main__.py` and `__init__.py` is empty. The cycle loop and the dashboard are both invisible to me.

Correct the recap and answer the two questions, and I'll seed the tree.
