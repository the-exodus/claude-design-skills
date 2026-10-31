# ADR-0004: A day runs from one midnight, included, to the next, excluded

**Status:** Accepted

## Context

The timetable lists sailings by day, and a sailing can depart exactly at midnight. Whether it belongs to the day that ends or the day that begins has to be decided once, for every function that splits time into days.

## Decision

A day is the half-open interval from its midnight, included, to the next midnight, excluded. A sailing departing at 00:00 belongs to the day that begins then, and to no other.

Rejected: an interval closed at both ends, because it lists a midnight sailing on two days.

## Consequences

Every function that selects by day compares `day_start <= t < day_end`.
