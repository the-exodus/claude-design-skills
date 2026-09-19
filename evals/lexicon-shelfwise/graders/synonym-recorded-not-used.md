---
# The merge is recorded in the surviving entry.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:patron)\*\*(?:[^\n]|\n(?!\s*\n))*?\bborrower\b'
flags: mi
---
