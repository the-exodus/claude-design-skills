# ADR-0004 — The archive is packed from logger dumps alone

**Status:** Accepted (2025-05-14)

## Context

Each gauge also keeps its own logger, which records the level every hour whether or not anyone asks. Field staff download it on their visits and save it as `dumps/<gauge>-<YYYY-MM>.csv`, and once a month `python -m archive.pack dumps/ YYYY-MM` packs that month's dumps into one file for the records office, which keeps the archive as the gauges' own record. Loggers miss hours: a flat battery, a full card.

## Decision

`archive/pack.py` packs the logger dumps exactly as they were logged and never uses gaugefeed's fetcher: an hour missing from a dump stays missing from the archive. The architecture tests enforce this boundary.

Filling a missing hour by fetching the station at packing time was rejected: the archive would hold a level read weeks later, filed under an hour it was never logged for, and the records office could not tell it from a logged one. Interpolating a missing hour from the hours either side was rejected for the same reason: a computed level would sit in the gauges' own record looking like a logged one.

## Consequences

The archive is the gauges' own record, gaps included, and packing it needs no network.
