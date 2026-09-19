---
# No source says days in lactation; the code and every doc say days in milk. True under rename and under retire.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:days in lactation)\*\*'
flags: mi
match: not_contains
---
