---
# Test 2: ordinary words.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:box|quantity)\*\*'
flags: mi
match: not_contains
---
