---
# A dated Update section is wrong for a decision change.
type: regex
target: { source: file, path: docs/adr/0001-store-readings-in-sqlite-and-back-up-nightly.md }
pattern: '^#+\s*Update\b|^\*{0,2}Update \d{4}'
flags: mi
match: not_contains
---
