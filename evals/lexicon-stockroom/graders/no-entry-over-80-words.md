---
# The bloated available entry (130 words) is cut down; the skill's own mark is about fifty.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){80}\S'
flags: m
match: not_contains
---
