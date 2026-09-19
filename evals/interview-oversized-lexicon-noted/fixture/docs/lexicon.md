# Lexicon

Every name used in gaugefeed, in one place.

---

**alert level** — The water level at which the flood page shows a station in amber.

**backfill** — Readings loaded after the fact from a station's own memory once it is reachable again.

**basin** — The river catchment a *station* belongs to.

**calibration** — The adjustment applied to a station's raw level to correct for its mounting height.

**cycle** — One run of gaugefeed over every station in the *station list*. Cycles are five minutes apart.

**dashboard** — The web page the duty hydrologist keeps open.

**datum** — The reference height a station's levels are measured from.

**duty hydrologist** — The person on call who watches the *dashboard*.

**fetch** — To ask a station for its current reading.

**fetch_all** — The function that fetches every station in the station list.

**fetch_reading** — The function that fetches one station.

**flood level** — The water level at which the flood page shows a station in red.

**flood page** — The public page that shows river levels.

**gauge** — See *station*.

**level** — The height of the water at a station, in metres above its *datum*.

**metered link** — A station connection billed per request.

**offset** — See *calibration*.

**operator** — The organisation that owns a *station*.

**outage** — A period in which gaugefeed itself cannot reach the network.

**peak** — The highest *level* a station reports during a flood.

**poll** — See *fetch*.

**raw level** — A *level* before *calibration*.

**reading** — One water level reported by a *station*, with the time gaugefeed fetched it. Not the time of measurement, which the stations do not report.

**readings dict** — The dictionary `fetch_all` returns, keyed by station URL.

**recession** — The falling limb of a flood, after the *peak*.

**stage** — See *level*.

**stale** — Said of a *reading* older than two *cycles*. A stale reading is still shown; it is not the same as having no reading.

**station** — A river gauge that answers requests for its current *reading*, identified by its URL.

**station list** — The *stations* gaugefeed asks each *cycle*, one URL per line.

**stations.txt** — The file holding the station list.

**telemetry** — The link between a station and the network.

**timeout** — How long gaugefeed waits for a station before giving up, five seconds by default.

**trend** — Whether a station's *level* is rising, steady or falling over the last hour.

**URLError** — The error raised when a station does not answer.
