---
# Decoy planted for THE-209: driver is an ordinary word, and the printer driver its users also meet is a sense nobody would apply to a person. Fails if it is kept, with or without an overload note.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:driver)\*\*'
flags: mi
match: not_contains
---
