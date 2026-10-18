# ADR-0003 — Share one database across reporting services

**Status:** Rejected (2026-04-15)

## Context

Account reports join data owned by four services. The reporting service
assembles them by calling each service's API, and a report for a large account
takes up to six minutes.

## Decision

**Move the four services' tables into one shared PostgreSQL database, and let
reporting query it directly.** Each service keeps write ownership of its own
tables.

Rejected: caching API responses in the reporting service. Reports must reflect
current data, and the cache would need invalidating on every change.

## Consequences

- A report becomes one query, and runs in seconds.
- Every schema change in the four services has to be checked against the other
  three and against reporting queries.
- The four services share one database's capacity and maintenance windows.

## Rejection

Sharing the database couples reporting and the other services to each service's
schema. [ADR-0001](0001-publish-cross-service-events-on-a-message-bus.md)
rejected that coupling when it ruled out consumers polling a producer's change
table. Reporting builds its own read model from ADR-0001's events instead.
