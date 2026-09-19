---
# The entry only restates ADR 0002's decision; its name is used nowhere else.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:click-to-focus policy)\*\*'
flags: mi
match: not_contains
---
