# ADR-0004 — The archive is packed from saved documents alone

**Status:** Accepted (2025-05-14)

## Context

The records office keeps a monthly archive of what the dashboard showed. Cron saves each cycle's document as `documents/<cycle time>.json`, beside gaugefeed rather than in it, and once a month `python -m gaugefeed.archive documents/ YYYY-MM` packs that month's documents into one file. Some cycles are never saved: the host was down, or the run hung.

## Decision

`gaugefeed/archive.py` packs the documents cron saved, exactly as they were printed, and never uses the fetcher: a cycle missing from the saved documents stays missing from the archive. The architecture tests enforce this boundary.

Filling a missing cycle by fetching the stations at packing time was rejected: the archive would hold readings that nobody saw on the dashboard, fetched weeks later and filed under a cycle time they never had. Rebuilding documents through the report from stored readings was rejected because gaugefeed stores no readings (ADR-0003).

## Consequences

The archive is a faithful record of what was shown, gaps included, and packing it needs no network. A gap can only be explained from outside gaugefeed, by the host's own logs.
