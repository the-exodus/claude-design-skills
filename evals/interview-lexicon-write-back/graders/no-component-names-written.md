---
# The names this design introduced stay out of the file.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: 'StationHealth|health\.py|health block'
flags: i
match: not_contains
---
