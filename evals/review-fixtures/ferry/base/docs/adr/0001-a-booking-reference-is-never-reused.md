# ADR-0001: A booking reference is never reused

**Status:** Accepted

## Context

The reference is printed on the ticket and quoted to the crew at the ramp. A passenger may still hold a printed ticket for a booking that was cancelled.

## Decision

References are issued from a counter that only goes up. A cancelled booking's reference is never issued again, even when that would keep references short.

## Consequences

References grow over a season. A reference on a ticket identifies one booking, ever, so the crew can turn away a cancelled ticket without a lookup by name.
