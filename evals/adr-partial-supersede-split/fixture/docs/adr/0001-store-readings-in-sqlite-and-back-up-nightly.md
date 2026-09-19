# ADR-0001 — Store readings in SQLite per station; back up nightly to object storage

**Status:** Accepted (2025-01-14)

## Context

Readings arrive from eleven gauges and are only ever queried per station or across a short window of all of them. The team has no database administrator, and the two earlier outages were both a shared PostgreSQL instance being unavailable. Nothing backed the readings up: a disk failure would have lost a station's whole history.

## Decision

**Storage.** Each station's readings live in their own SQLite file under `data_dir`. One shared PostgreSQL database was rejected because it put every station behind one server the team cannot staff.

**Backups.** Every night at 02:00 each station file is copied to the harbour authority's object storage, keeping thirty days. Backing up more often was rejected as unnecessary for data that changes every five minutes.

## Consequences

A station's data can be copied, restored or discarded without touching another's. Cross-station queries open eleven files and merge in the application. A disk failure loses at most one day of readings.
