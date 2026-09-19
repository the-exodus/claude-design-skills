# ADR-0004 — Reject readings older than twenty-four hours

**Status:** Accepted (2025-03-02)

## Context

A gauge that loses its uplink buffers readings and sends them all on reconnect. In February a gauge replayed nine days of readings, which redrew the public flood chart and paged the duty officer for a surge that had passed.

## Decision

A reading whose timestamp is more than twenty-four hours before its arrival is rejected and logged. Accepting it without alerting was rejected because the chart would still change under people who had already acted on it.

## Consequences

Long outages leave a permanent gap in a station's record. Short outages backfill as before. The rejected readings can be recovered from the log by hand if an investigation needs them.
