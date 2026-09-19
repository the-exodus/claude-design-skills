---
# A dated Update section is wrong for a decision change.
type: regex
target: { source: file, path: docs/adr/0002-poll-gauges-every-five-minutes.md }
pattern: '^#+\s*Update\b|^\*{0,2}Update \d{4}'
flags: mi
match: not_contains
---
