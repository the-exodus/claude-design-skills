---
# Test 3: lactation number is the same count as parity here, and is used nowhere.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:lactation number)\*\*'
flags: mi
match: not_contains
---
