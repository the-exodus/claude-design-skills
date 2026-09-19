---
# miss and silent are entries in the file's own shape.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^(?=[\s\S]*^\*\*miss\*\* [—–-] )(?=[\s\S]*^\*\*silent\*\* [—–-] )'
flags: m
---
