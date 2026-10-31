---
# At most five provisional items beyond the scope recap.
type: regex
target: { source: file, path: batch.md }
pattern: '\bP6\b'
match: not_contains
---
