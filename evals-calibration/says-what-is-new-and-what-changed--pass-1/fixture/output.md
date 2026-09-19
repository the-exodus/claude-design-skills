Written to `docs/lexicon.md`. 5 entries → 7, alphabetical ordering and the existing italic cross-reference style preserved.

**New — 2:**

> **miss** — A *cycle* in which gaugefeed asked a *station* and got no *reading*, whether it did not answer, answered too late, or answered with something gaugefeed could not read. A *cycle* in which gaugefeed did not ask is not a miss.

> **silent** — Said of a *station* that has gone an hour without a *reading*. It stays silent until it answers three times in a row, so one answer does not end it. Distinct from *stale*, which is the age of a *reading*, not whether the *station* answers.

**Changed — 0.** *cycle*, *reading*, *stale*, *station* and *station list* are byte-for-byte as they were. *stale* in particular is untouched, as you asked.

Three notes on the wording, since both entries are now shared vocabulary:

- **The second sentence of *miss* is the whole reason the term exists.** Once back-off ships, "gaugefeed has no reading from this station this cycle" covers two situations, and only one of them is a miss. Without that line every rule built on the word breaks quietly.
- **Both of silent's edges are in the entry**, because both change which stations the word picks out — a station that has answered once is still silent, and that is meaning, not behaviour. What's *not* in there is the polling consequence (silent ⇒ asked hourly); that's a decision, and it belongs in ADR-1 when you write it.
- **The distinction only points one way.** *silent* names *stale*; *stale* doesn't name *silent*, because pointing back would mean editing an entry whose meaning hasn't changed. Worth knowing it's asymmetric — if you later want the pair to cross-reference, that's a deliberate amendment to *stale*, your call.

Two things from the interview are still only in this conversation and die with it: the assumptions record (A2–A6 with falsification conditions, A3 being the one B13 hangs on) and the tracker lines for B11–B17. Say the word whenever.
