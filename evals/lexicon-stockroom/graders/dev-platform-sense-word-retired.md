---
# Decoy planted for THE-209: scan is an ordinary word, and the database's sequential scan is a sense nobody would apply to a carton. Fails if it is kept, with or without an overload note.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:scan)\*\*'
flags: mi
match: not_contains
---
