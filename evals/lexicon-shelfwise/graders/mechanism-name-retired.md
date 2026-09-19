---
# Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed or homed elsewhere.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:charge sweep)\*\*'
flags: mi
match: not_contains
---
