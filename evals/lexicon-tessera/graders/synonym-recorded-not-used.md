---
# The merge is recorded in the surviving entry.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:tile)\*\*(?:[^\n]|\n(?!\s*\n))*?\bpane\b'
flags: mi
---
