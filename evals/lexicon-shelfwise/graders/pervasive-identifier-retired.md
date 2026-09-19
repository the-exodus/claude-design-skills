---
# Decoy: ctx is in every file, and frequency in code is not test 2.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*request context'
flags: mi
match: not_contains
---
