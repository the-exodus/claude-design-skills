---
# Test 2: ordinary words.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:book|date)\*\*'
flags: mi
match: not_contains
---
