---
# feature query: no entry of its own. Label: retire (test 1, component behaviour); agreed by default (Part B).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*feature\ query\*\*'
flags: mi
match: not_contains
---
