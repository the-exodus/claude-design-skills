# 1. Reserve when the order is accepted, allocate when the wave is released

## Status

Accepted

## Context

Assigning bins at order time locked bins for hours before anyone picked
from them, and putaway into those bins had to wait.

## Decision

When an order line is accepted we reserve its quantity: the quantity is set
aside, but no bin is named. Bins are assigned only when the line's wave is
released, by allocation, earliest expiry first.

## Consequences

- A reservation never names a bin; only an allocation does.
- If the bins are emptied between reservation and release, allocation can
  come up short and the line stays reserved for the next wave.
