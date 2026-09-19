---
# Decoy: uow() is everywhere in the code, and frequency in code is not test 2.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:unit of work)\*\*'
flags: mi
match: not_contains
---
