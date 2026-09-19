# 0002. Late readings belong to the session they were taken in

## Status

Accepted, November 2022.

## Context

The parlour meters hold their readings when the network drops and send them
when it comes back. Most arrive within a minute. Some arrive after the
session has closed, and after a bad morning a few have arrived once the
afternoon session was already open.

The meter feed used to file each reading under whichever session was open
when it arrived. A cow could then show no morning milking and two afternoon
ones, her daily yield looked right while both session figures were wrong,
and the "not milked this session" check raised cows that had been milked.

## Decision

Every reading carries the time it was taken. A reading is filed under the
session in which it was taken, worked out from that time, whether or not
that session has closed and whatever session is open when the reading
arrives.

## Consequences

- A closed session's totals can still change. The daily yield report is
  final only the following morning.
- Closed sessions have to stay addressable by day and slot, not only "the
  current one".
- The withheld mark on a late milking is taken from the withhold list as it
  stands on arrival, which can differ from how it stood when the cow was
  milked. We accept this: a withdrawal that opened in between errs on the
  safe side, and one that ended in between is rare enough to correct by hand.
