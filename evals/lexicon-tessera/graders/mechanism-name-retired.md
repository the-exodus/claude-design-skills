---
# Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed or stays in its existing home.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:orphan sweep)\*\*'
flags: mi
match: not_contains
---
