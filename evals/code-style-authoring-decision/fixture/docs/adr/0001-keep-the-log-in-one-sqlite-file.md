# ADR-0001 — Keep the log in one SQLite file

**Status:** Accepted (2026-03-02)

## Context

The roastery has one laptop at the roaster and no server. The log must survive
a power cut mid-roast and be copied to the office by hand once a week.

## Decision

The whole log lives in one SQLite file, `roastlog.db`, written in WAL mode.

## Consequences

A copy of the file is a complete backup. Two laptops cannot share one log.
