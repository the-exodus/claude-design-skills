---
# The merge is recorded in the surviving entry.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:parity)\*\*(?:[^\n]|\n(?!\s*\n))*?lactation number'
flags: mi
---
