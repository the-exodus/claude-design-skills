---
# The bloated dry period entry (about 155 words) is cut down.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){80}\S'
flags: m
match: not_contains
---
