---
# registry: no entry of its own. Label: retire; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*registry\*\*'
flags: mi
match: not_contains
---
