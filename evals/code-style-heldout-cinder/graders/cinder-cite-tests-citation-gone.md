---
# The general test comment no longer cites a decision record.
type: regex
target: { source: file, path: tests/schedule_test.rs }
pattern: '0004'
match: not_contains
---
