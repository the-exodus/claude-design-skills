---
# No source says zoom; the code and every doc say promote.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:zoom)\*\*'
flags: mi
match: not_contains
---
