---
# The distinction survives and becomes two-sided: the original move entry does not name send.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:move)\*\*(?:[^\n]|\n(?!\s*\n))*?\bsend'
flags: mi
---
