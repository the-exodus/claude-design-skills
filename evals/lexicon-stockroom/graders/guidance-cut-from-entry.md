---
# The sales guidance is not meaning.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: 'call the warehouse'
flags: i
match: not_contains
---
