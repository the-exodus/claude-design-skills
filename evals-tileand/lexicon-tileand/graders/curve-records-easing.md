---
# The word not used stays recorded. One tuning run retired curve and stranded it.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*curve\*\*(?:[^\n]|\n(?!\s*\n))*?easing'
flags: mi
---
