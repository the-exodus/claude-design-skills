*reading* stands as defined — gaugefeed emits the fetch time, the dashboard consumes it. Noted, and it means the timestamp gaugefeed persists for silence and the one it prints in a reading are the same instant, not two clocks to reconcile.

## Lock 2 — recap

A **miss** is any cycle in which gaugefeed asked a station and got back no reading. Unreachable, timeout, HTTP error and malformed JSON all count identically; which one it was is diagnostic detail, not part of the rule.

**Silent** is a sticky per-station state with asymmetric edges. A station that is not silent becomes silent when an hour has passed since its last reading, on gaugefeed's clock, against a timestamp gaugefeed persisted itself. A station that is silent stops being silent after three readings in a row, counted in **asks, not cycles**. Between those two edges it holds whatever it is, regardless of what the elapsed-hour clock says — so a silent station that answers once is still silent, and a healthy station that misses twice is still healthy.

Polling follows from that state rather than forming part of it: a silent station is asked on the backed-off interval, but a silent station that has answered at least once since its last miss goes back to every cycle until it either completes three in a row or misses and drops back. One threshold, one hour, no ladder.

The reason silence is gaugefeed's state and not a line the dashboard draws is metered links: two of the stations that die are billed per request, so the knowledge has to sit where the request decision is made.

**One amendment:** I'm dropping "usable" and writing the rule in terms of *reading* alone. Your lexicon already defines a reading as a water level plus a fetch time — a malformed response isn't a degraded reading, it's no reading. "Usable reading" reads like a second, weaker category that doesn't exist. Say if you meant a real distinction there (a 200 with a null level, say) and I'll reopen; otherwise the rule is "no reading."

## Closed — decided

**Fork.** Alternatives on the table: (a) expose last-success-time per station and let the dashboard decide what's silent — rejected, metered links mean gaugefeed must act on the knowledge, not just report it; (b) threshold on consecutive miss count rather than elapsed time — rejected, a miss count stops meaning the same thing once back-off stretches the spacing between asks; (c) symmetric edges, silence ends when a reading arrives — rejected, it yo-yos the polling interval for a flapping station and hysteresis is the point.

**Sub-branch, deferred-later:** the station that answers every 59 minutes never trips entry and never accumulates three in a row, so it reads permanently healthy while being useless. Out of this version. **Resolves when** someone needs a freshness guarantee on the dashboard rather than an aliveness signal; as it stands the dashboard's existing *stale* greying is the only thing that would hint at it. Tracker candidate.

**Lexicon:** *silent* goes in, with the two edges as its definition. Nothing else.

**ADR-worthy**, flagged for Phase 8: real fork, the rejection reasons outlive the change, and a future reader looking at a state machine with mismatched edges will absolutely ask why.

## What closing it changed

- **Persisted state is three fields, not one:** last reading time, consecutive-successes, and the sticky silent flag. Both edges and the polling decision are functions of those three. That's smaller than I expected and it firms up the deep-module case — one thing owning station health and the ask decision, rather than a tracker, a scheduler and a formatter all reading the same record.
- **Two branches collapse into one.** "Never answered" now has two ways to happen: a station newly added to `stations.txt`, and a rebuilt host with no state file. Both produce a record with no last-reading time, and both need the same answer. Merged.
- **New probe for back-off:** a flapper on a metered link answers once, gets promoted to every-cycle polling, then misses. Bounded extra cost, but non-zero, and it's exactly the stations you're trying to save money on.
- **Condition recheck:** state outliving a version now definitely holds. The evolution/compatibility branch isn't prunable.

## Next: the output contract

Foundational — the dashboard branch and the back-off branch both write into it, and it's where `fetch_all`'s current contract dies. Absence currently means "didn't answer"; with back-off it would also mean "deliberately not asked", and those two must not look alike to the dashboard.

1. Does every station in `stations.txt` appear in the output every cycle now, whatever happened to it — or is the readings dict left alone and health reported alongside it?
2. How much does the output carry beyond the state itself? "Silent" alone lets the dashboard put a marker up; "silent since 09:40, last tried 10:15, 14 misses" is what you want when someone finally does phone. Is the JSON file the diagnosis surface too, or is that a log?
3. Does the fetching layer own the state file — read it, decide who to ask, write it back — or does something above it load state and hand it in? This is the decision-hiding question: if fetching owns it, one module knows everything about station health; if not, the caller has to understand the state machine to drive it correctly.
4. The dashboard is a separate repo on its own release cycle, and cron runs gaugefeed every five minutes regardless. When the new JSON shape first lands, what does the old dashboard do with it — and which side deploys first?
5. Fork: two shapes I can see. Keep `{url: reading}` exactly as it is and add a sibling health block, which the current dashboard would ignore harmlessly; or restructure so each station is an object with an optional reading inside it, which is cleaner but breaks the consumer on the first cycle. What would you add to that?
