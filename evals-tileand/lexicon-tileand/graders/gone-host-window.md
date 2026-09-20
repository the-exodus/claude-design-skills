---
# host window: no entry of its own. Label: retire; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*host\ window\*\*'
flags: mi
match: not_contains
---
