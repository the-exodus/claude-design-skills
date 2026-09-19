*Usable* dropped; the rule reads "no reading" throughout, and the lexicon entry for *miss* below uses that wording.

## Lock 2 — recap

Gaugefeed's output grows a sibling `health` block alongside the existing `{url: reading}` map, which keeps its shape exactly. Every station in the *station list* gets a health entry every cycle, carrying three things: its state, since when, and when it was last asked. Everything else an operator might want — which failure it was, how many misses, what the timeout was — goes to the log, not the file.

`gaugefeed/health.py` holds a `StationHealth` class that owns the state file in `/var/lib/gaugefeed` end to end: it reads it, decides which stations this cycle asks, takes back the results, and writes it out. `fetch_all` calls it, and no other code knows that a state machine exists.

The dashboard deploys first, tolerating an absent `health` block by behaving exactly as it does today; gaugefeed starts emitting it afterwards. No flag day, no coordinated release.

## Lock 3 — adversarial, and one clarification it forces

**"Every station every cycle" applies to the health block, not the readings map.** These two answers collide if read literally: the readings map keeps its current shape, but a station that wasn't asked has no reading to put in it. Filling the gap with nulls is the obvious move and it's the one thing that breaks your compatibility story — the old dashboard's promise is that it ignores *fields it doesn't recognise*, which is not the same as surviving a null where it expects an object. So the readings map stays sparse, exactly as today, and the health block is the complete one. Completeness lives in the new structure, which is the whole reason for adding it.

**Second finding, which I'm moving rather than resolving:** "since when" is ambiguous between the last reading's time and the moment the state flipped, and those differ by up to a cycle — more once back-off stretches the spacing. It's also undefined for a station that has never answered at all. That's the merged never-answered case resurfacing in the output shape. It's a question about what a reader of the dashboard is being told, so it goes to the branch you've asked for next rather than holding this one open.

## Closed — decided

**Fork.** Rejected: restructuring each station into an object with an optional reading inside. Cleaner shape, and it breaks the consumer on the first cycle after deploy with no ordering that avoids it.

**Cost recorded.** The sibling block means two maps keyed by URL that a reader has to join per station, and nothing structurally prevents them disagreeing. That's the price of not breaking the consumer, paid deliberately. If the dashboard's shape is ever revisited, folding them is the obvious cleanup.

**Decomposition consequence:** serialising the health block belongs to `health.py` too, not to whatever prints the JSON. If the printer assembles that structure, it has to know the state names and what "since" means, and the state machine has leaked into the one module you just said shouldn't know about it.

**Deferred-implementation:** `fetch_all`'s internal signature — tuple, dataclass, whatever. One constraint from the design: fetching and the state write happen under one call, so the caller can't get readings without the health that goes with them.

**Lexicon: one admitted, 7 → 8.** ***station health*** — what `StationHealth` keeps for each *station*: its state, since when, and when it was last asked.

**ADR-worthy** — likely the same ADR as the silence rule rather than its own. The fork is real and the compatibility reasoning is what a future reader will want when they find two parallel maps.

**New sub-branch seeded:** the state file accumulates records for stations no longer in the *station list* — an inevitability given that editing a URL mints a new station. Pruning or not is an evolution question; parked for the durability branch.

---

## Next: dashboard representation, against *stale*

The sharp part. *Stale* is already defined, already implemented, and fires at two cycles — ten minutes. *Silent* fires at an hour. So silence is a strict subset of staleness in time: **every silent station is already greyed out before it goes silent**, and you're adding a second indicator on top of an existing one that already covers the same ground more eagerly.

Worth noting your recovery rule dodges the worst version of this. If back-off applied to stations that were answering, everything on a slow interval would be permanently stale by definition; promoting a station back to every-cycle polling the moment it answers once means the slow interval only ever applies while it has nothing to show anyway. The collision survives in one spot: a station that answers once, drops back to hourly on the next miss, and now sits there stale, silent, and holding a five-minute-old number.

Probes:

1. **What does silent do to the grey?** Replace it, compound it, or does *stale* need its definition changed now that a stronger signal exists above it? Changing an implemented, inherited lexicon term is on the table but it's your call, not a side effect.
2. **Does a silent station still show its last number at all?** Your opening complaint was a stale number with no hint anything is wrong. Greying a number that is three days old is arguably still that bug.
3. **The recovering station shows a fresh reading and is still flagged silent** — that's your hysteresis made visible, and it will look like a contradiction to anyone reading the board. Is it distinct on screen, is the recovery progress visible at all, or does it just render as healthy while gaugefeed keeps the flag internally?
4. **A station that has never answered** — new line in `stations.txt`, or a rebuilt host — renders as what? It has no number to grey and no "since".
5. **Does anything make silence noticeable without scanning?** "Nobody finds out until someone phones" is a *noticing* failure. A per-station marker fixes the board and doesn't obviously fix that.
6. **The "since" question from above:** last reading time, or the moment the state flipped?
7. **Fork:** one axis — silence as an intensification of the existing staleness rendering, ageing from grey to gone, with no second concept on screen. Or two axes — freshness and aliveness as independent things a station has. The first is less to explain and reuses what's built; the second is the only one that can say "answering fine, but we're only asking hourly." What else is on the table?

One scoping line: the dashboard is a separate repo, so I'm designing what gaugefeed's output must carry for that repo to render any of this, and treating the actual visual treatment as theirs. Say if the rendering is yours too and in scope for this interview.
