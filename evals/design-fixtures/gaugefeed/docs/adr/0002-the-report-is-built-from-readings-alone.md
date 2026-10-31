# ADR-0002 — The report is built from readings alone

**Status:** Accepted (2025-03-10)

## Context

The dashboard reads one JSON document per cycle, and its layout changes more often than anything else in gaugefeed. Changes to it are easiest to make and review when the document can be built and checked from a handful of readings written by hand.

## Decision

`gaugefeed/report.py` builds the document from what it is handed: the cycle's readings, keyed by station URL, and the cycle's time. It imports no other gaugefeed module and does no I/O: it neither fetches, reads files, nor looks at the clock. The architecture test keeps it that way: its allow-list gives the report no gaugefeed module to import, so a new dependency fails the build.

Letting the report call the fetcher itself was rejected because every test of the document would then need the network patched. Reading the clock inside the report was rejected because the cycle's time would differ between the report and anything else that records it, and the tests could not fix it.

## Consequences

The document is tested with plain dicts and a fixed time. Anything new the dashboard shows has to reach the report as data from `__main__`, so a feature that needs more than the readings changes what the report is handed, not what it imports.
