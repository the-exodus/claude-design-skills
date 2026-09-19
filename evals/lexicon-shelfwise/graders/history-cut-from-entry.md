---
# The pilot sentence is history, not meaning.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '2023 pilot|ten days to seven'
flags: i
match: not_contains
---
