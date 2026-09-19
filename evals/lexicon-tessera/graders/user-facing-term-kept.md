---
# Decoy: split ratio has a config key but is a word users say and set.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:split ratio)\*\*'
flags: mi
---
