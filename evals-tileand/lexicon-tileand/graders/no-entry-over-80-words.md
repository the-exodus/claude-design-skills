---
# gather stood at 160 words and focused member at 132; the skill's own mark is about fifty. Bold header labels that end in a colon are not entries.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*[^*\n]*[^:*\n]\*\*(?:[ \t]+|\n(?![ \t]*\n))(?:\S+(?:[ \t]+|\n(?![ \t]*\n))){78}\S'
flags: m
match: not_contains
---
