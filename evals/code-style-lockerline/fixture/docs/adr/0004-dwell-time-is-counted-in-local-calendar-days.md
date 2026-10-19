# ADR-0004: Dwell time is counted in local calendar days from the door locking

**Status:** Accepted (2026-02-17)

## Context

Customers are told "you have three days". They count calendar days where the
bank is, not 24-hour periods.

## Decision

Dwell time is the number of local midnights at the bank's site since the door
locked at drop-off. It is not counted from the courier's scan, which can come
minutes before the door is closed.

## Consequences

A parcel dropped at 23:59 has a dwell time of one day at 00:00.
