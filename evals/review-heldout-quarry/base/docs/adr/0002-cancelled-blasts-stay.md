# 0002. Cancelled blasts stay in the schedule

Status: Accepted

## Context

The planning permission requires a blast log that can be inspected. A blast
that was planned and notified but then cancelled is part of that history.

## Decision

Cancelling sets a blast's status to `cancelled`; blasts are never removed
from the schedule. A blast id identifies one planned firing and is never
reused. Cancelled and fired blasts are ignored by the spacing rule.

## Consequences

The schedule only grows. Lookups by id must expect cancelled entries.
