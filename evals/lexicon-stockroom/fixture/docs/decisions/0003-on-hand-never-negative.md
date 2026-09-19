# 3. On-hand never goes negative

## Status

Accepted

## Context

Pickers and counters post movements against the same bin at the same time.
Before this decision a bin could show -3 on-hand until someone noticed.

## Decision

Inside every movement's unit of work, the source bin's on-hand is re-summed
from the ledger and the movement is rejected if it would take on-hand below
zero. We call this check the reconciliation sweep; the name is left over
from the nightly job it replaced.

## Consequences

- On-hand is never negative, for any bin, at any time.
- A picker whose pick is rejected is sent to recount the bin.
