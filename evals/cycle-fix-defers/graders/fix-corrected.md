---
# Fixed: a midnight sailing is listed on its own day (half-open interval).
type: regex
target: { source: file, path: ferrybook/schedule.py }
pattern: 'day_start <= s\.departs < day_end'
---
