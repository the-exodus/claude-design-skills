---
# The entry only restates decision record 0002; its name is used nowhere else.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:late-reading rule)\*\*'
flags: mi
match: not_contains
---
