# ADR-0002 — Poll gauges every five minutes

**Status:** Accepted (2025-02-03)

## Context

The gauges in service expose a read-only HTTP endpoint and cannot push. The pilots need a level no more than ten minutes old; the flood page tolerates fifteen.

## Decision

Tidewatch asks each gauge for its current reading every five minutes. Polling faster was rejected because the oldest gauges drop requests when asked more than once a minute, and slower would miss the pilots' ten-minute bound after one failed poll.

## Consequences

One missed poll still leaves a reading inside the pilots' bound. Load on the gauges is fixed and predictable. A reading is on average two and a half minutes old when it is shown.
