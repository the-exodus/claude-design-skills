---
# Test 3: pane is a synonym of tile and is used nowhere.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:pane)\*\*'
flags: mi
match: not_contains
---
