---
# Test 2: an ordinary word. shortcut is not graded: the owner accepts it kept with its sense stated (THE-212).
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:config file)\*\*'
flags: mi
match: not_contains
---
