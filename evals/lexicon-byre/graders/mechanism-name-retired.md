---
# Mechanism vs guarantee: the routine's name is not a headword, whether the guarantee is reframed (withhold list) or stays in its existing home.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:withhold sweep)\*\*'
flags: mi
match: not_contains
---
