# 3. Serve holds in queue order with a fixed pickup window

Date: 2023-07-19

## Status

Accepted

## Context

Staff allocated returned items to waiting holds by hand, and patrons who
placed a hold first were sometimes served after later ones. Items set aside
for patrons who never came sat on the hold shelf indefinitely.

## Decision

Holds on a title are served in the order they were placed. When an item is
ready for a patron, the patron has `holds.pickupWindowDays` days (default 7)
to collect it. The patron is notified when the item is ready and reminded the
day before the window closes. A hold that is not collected within the window
lapses and the item passes to the next hold in the queue; the patron whose
hold lapsed keeps no place in the queue.

## Consequences

- Staff cannot lengthen an individual patron's window.
- A patron who misses the window must place a new hold, at the back of the
  queue.
