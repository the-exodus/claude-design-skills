---
# Decoy: Env is in 10 of 11 Go files, and frequency in code is not test 2.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:Env)\*\*'
flags: m
match: not_contains
---
