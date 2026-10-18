# ADR-0002: Compartment status codes are fixed integers

**Status:** Accepted (2026-01-20)

## Context

The courier app, which we do not build, reads each compartment's status as an
integer over the bank's status endpoint and shows a different screen for each.

## Decision

Status codes are fixed integers, defined once in `StatusCodes`, and never
renumbered. A new status takes a new number.

## Consequences

The courier app can be updated on its own schedule.
