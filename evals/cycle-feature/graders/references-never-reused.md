---
# Fixed: references come from a counter again (ADR-0001).
type: regex
target: { source: file, path: ferrybook/booking.py }
pattern: 'max\(self\._bookings'
match: not_contains
---
