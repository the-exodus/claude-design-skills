# ADR-0003: Expiry is settled lazily, never by a timer

**Status:** Accepted

## Context

Anything in Ferrybook that lapses with time (an offer, a hold, a reservation) could be expired by a background timer or thread, or settled when the book is next consulted. Ferrybook runs as a single-threaded service behind the ticket office, and its tests drive time with a fake clock.

## Decision

Nothing in Ferrybook starts a timer or a thread. Whatever has lapsed is settled at the start of each operation that reads or changes the bookings, against the clock the book was given. Between operations, a lapsed item may still be in memory; no reader can observe it, because every reader settles first.

Rejected: a background thread that expires items on time, because it would make every operation concurrent with it and the tests depend on wall-clock timing.

## Consequences

A lapsed item lingers in memory until the next operation. Every public operation must settle first; one that forgets can observe or act on a lapsed item.
