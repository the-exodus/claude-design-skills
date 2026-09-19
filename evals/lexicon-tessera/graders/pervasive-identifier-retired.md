---
# Decoy: ctx is in 8 of 11 source files, and frequency in code is not test 2.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:context)\*\*'
flags: mi
match: not_contains
---
