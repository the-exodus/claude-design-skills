---
# The header's admission rule ('appears in the code, or a decision introduced it') is replaced by the tests.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: 'appears in the\s+code'
flags: i
match: not_contains
---
