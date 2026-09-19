---
# Mechanism vs guarantee: the sweep's name is not a headword, whether the guarantee is reframed or homed elsewhere.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:reconciliation sweep)\*\*'
flags: mi
match: not_contains
---
