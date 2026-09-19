---
# The header's admission rule ('or a decision defined it') is replaced by the tests.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: 'a decision defined it'
flags: i
match: not_contains
---
