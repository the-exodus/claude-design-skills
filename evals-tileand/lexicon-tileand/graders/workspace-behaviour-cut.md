---
# The owner's ruling of 2026-09-20, reversing his first label: 'created on demand, evaporates when empty' is behaviour, visible to nothing that talks, and goes. The term stays (kept-workspace).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*workspace\*\*(?:[^\n]|\n(?!\s*\n))*?(?:evaporat|on demand)'
flags: mi
match: not_contains
---
