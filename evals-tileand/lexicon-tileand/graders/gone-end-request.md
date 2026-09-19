---
# end request: no entry of its own. Label: retire (test 1, mechanism; 'request' now distinguishes it); agreed by default (Part B).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*end\ request\*\*'
flags: mi
match: not_contains
---
