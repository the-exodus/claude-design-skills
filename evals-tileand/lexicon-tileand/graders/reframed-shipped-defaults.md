---
# default rules becomes shipped defaults: the label says the word it lands on is an entry.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*shipped\ defaults\*\*'
flags: mi
---
