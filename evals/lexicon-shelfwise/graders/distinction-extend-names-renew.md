---
# The distinction survives: each entry names the other.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:extend)\*\*(?:[^\n]|\n(?!\s*\n))*?\brenew'
flags: mi
---
