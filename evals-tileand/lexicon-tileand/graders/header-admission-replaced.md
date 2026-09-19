---
# The header admitted a word because 'a decision defined it'.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: 'or a decision defined\s+it'
flags: i
match: not_contains
---
