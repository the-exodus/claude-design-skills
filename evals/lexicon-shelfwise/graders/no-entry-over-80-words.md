---
# The bloated pickup window entry (about 140 words) is cut down; the skill's own mark is about fifty.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){80}\S'
flags: m
match: not_contains
---
