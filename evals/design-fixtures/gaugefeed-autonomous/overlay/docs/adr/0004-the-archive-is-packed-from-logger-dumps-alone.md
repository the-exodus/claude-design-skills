# ADR-0004 — The archive is packed from logger dumps alone

**Status:** Accepted (2025-05-14)

## Context

Each gauge also keeps its own logger, which records the level every hour whether or not anyone asks. Field staff download it on their visits and save it as `dumps/<gauge>-<YYYY-MM>.csv`, and once a month `python -m gaugefeed.archive dumps/ YYYY-MM` packs that month's dumps into one file for the records office, which keeps the archive as the gauges' own record. Loggers miss hours: a flat battery, a full card.

## Decision

`gaugefeed/archive.py` packs the logger dumps exactly as they were logged and never uses the fetcher: an hour missing from a dump stays missing from the archive. The architecture tests enforce this boundary.

Filling a missing hour by fetching the station at packing time was rejected: the archive would hold a level read weeks later, filed under an hour it was never logged for, and the records office could not tell it from a logged one. Packing the dashboard's documents instead of the dumps was rejected because they hold one fetched reading per cycle, only for the stations that answered: what the dashboard showed, not what the gauge logged.

## Consequences

The archive is the gauges' own record, gaps included, and packing it needs no network. Nothing the dashboard shows depends on it.
