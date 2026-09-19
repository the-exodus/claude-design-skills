---
# The owner's label: 'created on demand, evaporates when empty' is part of what a workspace is here.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*workspace\*\*(?:[^\n]|\n(?!\s*\n))*?(?:evaporat|on demand)'
flags: mi
---
