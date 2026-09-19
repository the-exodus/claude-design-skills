---
# Windowing: no entry of its own. Label: retire (test 1, module); agreed by default (Part B).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*Windowing\*\*'
flags: mi
match: not_contains
---
