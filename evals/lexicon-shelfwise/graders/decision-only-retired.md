---
# The entry only restates ADR-0004's decision.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:patron-first policy)\*\*'
flags: mi
match: not_contains
---
