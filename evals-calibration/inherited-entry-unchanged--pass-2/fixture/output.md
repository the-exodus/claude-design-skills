## Lock 2 — recap

Gaugefeed's `health` block carries one entry per station in the *station list*, every cycle, with three fields:

- **state** — one of three: answering, silent, or no reading yet. Three rather than two because a station that has never answered can't be silent under the entry rule (there's no last reading to measure an hour from) and obviously isn't answering.
- **since** — the moment the station entered that state, on gaugefeed's clock. Not the last reading's time.
- **last asked** — when gaugefeed last made a request to it.

Everything else the board needs is already there or derives from those. **Freshness needs no new field**: each reading already carries its fetch time, so age and the existing *stale* greying come off the readings map, and the aliveness axis comes off `health.state`. The two axes read from two different places, which is what makes them independent. **The silent count at the top of the board is derived** by the dashboard counting entries in the block. **The last known number stays in the dashboard's memory** — gaugefeed does not carry last-known readings in its output, because that would duplicate the readings map and deepen the cost already recorded on the sibling-block decision.

A recovering station therefore renders as a fresh, ungreyed number with a silent marker beside it, until three in a row promote it. No progress toward those three is emitted; the count stays inside `health.py`.

## Lock 3 — adversarial

**Three findings. Two I'm closing on, one I'm moving.**

**1. The output needs a cycle timestamp, and doesn't have one.** `last asked` only answers the question you added it for — "asked and failed" versus "deliberately not asked" — if the reader can compare it against *this* cycle's time. The dashboard can't reliably reconstruct that: it could take the newest fetch time in the readings map, except on a cycle where nothing answered there are none, which is exactly the cycle that matters. Approximating with its own file-pickup time works until the cron run is slow or the file sits. So: one top-level timestamp for the cycle, written when the cycle starts. Cheap, and it makes every other time in the file interpretable against a common instant. That's my addition, not something you said — say if you'd rather the dashboard guess.

**2. "No reading yet" has to age into silent, or the design reintroduces its own bug.** Consider the rebuilt host: the state file is gone, every station starts with no record and no last-reading time. If no-reading-yet is a terminal state that only a first reading can leave, then a station that is genuinely dead at the moment of the rebuild reads "no reading yet" forever, never enters the silent count, and nobody finds out until someone phones. So the hour clock starts at record creation when there's no reading to start it from: a station that has never answered goes silent an hour after gaugefeed first heard of it, whether it's new in `stations.txt` or new because the host was rebuilt. No-reading-yet is transient, up to an hour, and `since` for such a record is its creation time. That also gives `since` a defined value in the one case where it had none.

**3. The board wants to say "answering, but we only ask hourly" — and nothing in this block says the interval.** The dashboard can infer it (state is silent, therefore hourly), but that hardcodes gaugefeed's back-off policy into the other repo, and the day the policy changes the board starts lying with no code change on its side. The fix is a field carrying the current interval or the next scheduled ask. I'm not closing it here — it's the back-off branch's policy to expose, and that branch is next. Recorded as a probe there.

## Closed — decided

**Fork.** Rejected: silence as an intensification of the existing staleness rendering — grey ageing toward gone, one concept on screen. Less to explain and reuses what's built, but it cannot express "answering fine, we're just asking hourly", because on a single freshness axis a backed-off station and a dead one are the same pixel. Two axes chosen: freshness from the reading's fetch time, aliveness from `health.state`.

**Consequence worth stating:** a silent station shows two times that differ by roughly the threshold — its reading's age, and how long it's been silent. That's inherent in `since` meaning the flip moment rather than the last reading, which you chose deliberately. It's not a bug; it will be asked about.

**Also:** on a dashboard restart during silence, the remembered number is gone, so the station renders silent with no number — on screen, the same as a station in its first hour. The `state` field still distinguishes them in the data, so this is a rendering call in your other repo, not a gap in what gaugefeed emits.

**Persisted state is now five fields, not the three I said last turn:** last reading time, consecutive successes, state, since, last asked. `since` and `last asked` can't be reconstructed by a fresh process, so they persist or they don't exist.

**Lexicon: nothing admitted, still 7.** The three state values are the data contract's vocabulary, which is structure, not meaning — same rule that kept "health block" out. *Age* is the ordinary word.

**ADR-worthy**, with the output-contract ADR rather than the silence-rule one: the two-axes fork and the reason the single-axis option can't express back-off belong next to the sibling-block compatibility reasoning.

## What closing it changed

Finding 2 collapses the merged never-answered case into the silence rule itself — the hour clock just has two possible starting points. That resolves most of what I parked for the durability branch; what's left there is the state file being corrupt rather than absent, plus pruning records for stations no longer in the list.

Finding 1 adds a top-level field to a contract I closed last turn. It's additive and the old dashboard ignores unknown fields, so the compatibility story is unchanged and I'm not reopening that branch — noting the amendment rather than treating it as a reopen.

---

## Next: back-off policy

The last branch that can still change the output shape, and three deferrals now point at it.

1. **What is the backed-off interval, and is it fixed or escalating?** An hour matches the threshold, which is tidy but means a station goes silent and gets retried almost immediately. Days of silence at a fixed hourly rate is still 24 requests a day on a metered link.
2. **Is there a floor and a ceiling?** A station silent for three months — does the interval keep growing, and if so does it ever stop asking entirely? A station never asked again can never recover, which is a trap worth naming before it's built.
3. **The promoted flapper.** A silent station on a metered link answers once, jumps to every-cycle polling, then misses on the next cycle and drops back. Worst case it costs 12 requests an hour instead of 1, on exactly the stations you're economising on. Bounded, but is the bound acceptable, or does recovery need to be gentler than straight to every cycle?
4. **Does the interval survive a restart?** It's a function of the persisted state, so mechanically yes — but on a rebuilt host every station is no-reading-yet and asked every cycle for the first hour, metered ones included. Acceptable?
5. **Alignment.** Cron gives five-minute ticks; an hourly station is asked on whichever tick crosses the hour. Does anything care whether that's a consistent wall-clock slot, or is "at least an hour since we last asked" enough?
6. **Finding 3 above:** does the health entry carry the interval or the next scheduled ask, or does the dashboard infer it from the state?
7. **Fork:** interval as a function of the state (silent ⇒ hourly, one rule, no extra storage), or a per-station backoff value that grows with consecutive misses and is persisted. The first is simpler and `health.py` needs no new field; the second is the only one that can back off further over days. What else is on the table?
