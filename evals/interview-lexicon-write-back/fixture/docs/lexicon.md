# Lexicon

The words someone needs defined to talk about using or developing gaugefeed.

---

**cycle** — One run of gaugefeed over every station in the *station list*. Cycles are five minutes apart.

**reading** — One water level reported by a *station*, with the time gaugefeed fetched it. Not the time of measurement, which the stations do not report.

**stale** — Said of a *reading* older than two *cycles*. A stale reading is still shown; it is not the same as having no reading.

**station** — A river gauge that answers requests for its current *reading*, identified by its URL.

**station list** — The *stations* gaugefeed asks each *cycle*, one URL per line.
