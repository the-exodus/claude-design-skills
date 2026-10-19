---
# The doc on Schedule::segments, a restatement of its name, is gone.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'Returns[\s/]+the[\s/]+schedule.s[\s/]+segments'
flags: i
match: not_contains
---
