---
# The distinction survives: each entry names the other.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:send)\*\*(?:[^\n]|\n(?!\s*\n))*?\bmove'
flags: mi
---
