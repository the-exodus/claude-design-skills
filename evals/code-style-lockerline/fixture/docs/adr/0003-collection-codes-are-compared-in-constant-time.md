# ADR-0003: Collection codes are compared in constant time

**Status:** Accepted (2026-02-03)

## Context

The scanner beeps when the bank has answered. Anyone standing at the bank can
time the beep.

## Decision

A scanned code is compared with the compartment's code in constant time.

## Consequences

The comparison cannot use `String.equals`.
