---
# The new entries state meaning, not how it is built.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*(?:miss|silent)\*\*(?:[^\n]|\n(?!\s*\n))*?(?:state file|/var/lib|\bflag\b|\bfield\b|\bJSON\b|\bcron)'
flags: mi
match: not_contains
---
