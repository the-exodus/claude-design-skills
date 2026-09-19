---
# interop layer: no entry of its own. Label: retire (test 1, layer); agreed by default (Part B).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*interop\ layer\*\*'
flags: mi
match: not_contains
---
