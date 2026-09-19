# 2. Compute available on read

## Status

Accepted

## Context

Available used to be a stored counter updated on every reservation and
movement. During the 2024 peak the counter went stale and sales promised
stock that was not there.

## Decision

Available is computed on read from the ledger and the open reservations.
There is no stored column.

## Consequences

- Reading available costs a query; the SKU endpoint is not cached.
- There is nothing to repair when a counter drifts, because there is none.
