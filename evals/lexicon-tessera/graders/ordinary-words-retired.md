---
# Test 2: ordinary words.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:config file|shortcut)\*\*'
flags: mi
match: not_contains
---
