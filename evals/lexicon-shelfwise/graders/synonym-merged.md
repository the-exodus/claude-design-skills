---
# Test 3: borrower is a synonym of patron.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:borrower)\*\*'
flags: mi
match: not_contains
---
