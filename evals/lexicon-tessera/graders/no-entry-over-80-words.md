---
# The bloated layout entry (about 160 words) is cut down.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){80}\S'
flags: m
match: not_contains
---
