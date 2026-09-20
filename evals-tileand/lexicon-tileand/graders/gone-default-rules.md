---
# default rules: no entry of its own. Label: rename -> shipped defaults; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*default\ rules\*\*'
flags: mi
match: not_contains
---
