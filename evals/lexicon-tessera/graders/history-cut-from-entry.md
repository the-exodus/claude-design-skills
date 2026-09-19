---
# Why the default layout changed is history, not meaning.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: 'ultrawide|until 0\.4|off-cent'
flags: i
match: not_contains
---
