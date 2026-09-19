---
# The old status is replaced, not kept beside the new one.
type: regex
target: { source: file, path: docs/adr/0002-poll-gauges-every-five-minutes.md }
pattern: '^(?:\*\*Status:\*\* |Status: )?Accepted\b'
flags: m
match: not_contains
---
