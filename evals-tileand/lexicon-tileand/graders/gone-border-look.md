---
# border look: no entry of its own. Label: retire (test 1, data structure); agreed by default (Part B).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*border\ look\*\*'
flags: mi
match: not_contains
---
