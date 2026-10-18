# ADR-0002 — The report floors the development ratio

**Status:** Accepted (2026-04-11)

## Context

Roasters compare the printed day report with the roaster's own screen, which
shows the development ratio as a whole percent, floored.

## Decision

The report floors the development ratio to a whole percent. It never rounds.

## Consequences

A ratio of 19.9 % prints as 19 %, as it shows on the screen.
