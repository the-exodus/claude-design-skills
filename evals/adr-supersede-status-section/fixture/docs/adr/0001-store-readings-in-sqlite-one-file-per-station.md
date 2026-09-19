# ADR-0001 — Store readings in SQLite, one file per station

**Status:** Accepted (2025-01-14)

## Context

Readings arrive from eleven gauges and are only ever queried per station or across a short window of all of them. The team has no database administrator, and the two earlier outages were both a shared PostgreSQL instance being unavailable.

## Decision

Each station's readings live in their own SQLite file under `data_dir`. A rejected alternative was one shared PostgreSQL database: it made the cross-station queries simpler but put every station behind one server the team cannot staff.

## Consequences

A station's data can be copied, restored or discarded without touching another's. Cross-station queries open eleven files and merge in the application. Schema changes have to be applied file by file.
