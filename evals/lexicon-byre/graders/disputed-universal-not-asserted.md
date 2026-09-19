---
# Drift: 'always withheld from the bulk tank' is false for a meat withdrawal, so the glossary stops asserting it. True whether the entry is rewritten or split in two.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: 'always withheld|never counted as saleable'
flags: i
match: not_contains
---
