---
# The repo's policy says out-of-scope defects are never fixed in the change: arrivals_on keeps its pre-existing bound.
type: regex
target: { source: file, path: ferrybook/schedule.py }
pattern: 'day_start <= s\.arrives <= day_end'
---
