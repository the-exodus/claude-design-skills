# ADR-0004: Refunds are paid in whole kroner

**Status:** Accepted

## Context

The card terminal at the ticket office refunds whole kroner only, and passengers who cancel within the cancellation window are owed 80% of what they paid.

## Decision

A refund is computed in kroner: `round(paid / 100 * 0.8)`, and paid out as whole kroner. The refund is recorded against the booking in kroner.

Rejected: computing the refund in øre and rounding down to whole kroner at the terminal, because staff would have to explain the difference to passengers.

## Consequences

Refunds may be up to 50 øre more or less than 80%. Settlement with the port authority counts refunds in kroner.
