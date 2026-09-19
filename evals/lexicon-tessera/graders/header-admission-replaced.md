---
# The header's admission rule (anything the team has given a name) is replaced.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: 'given something a\s+name'
flags: i
match: not_contains
---
