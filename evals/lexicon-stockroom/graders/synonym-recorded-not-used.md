---
# The merge is recorded in the surviving entry.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:SKU)\*\*(?:[^\n]|\n(?!\s*\n))*?\bitem code\b'
flags: mi
---
