---
# The overload that earns stack its entry. One tuning run dropped it; the round judge said keep.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*stack\*\*(?:[^\n]|\n(?!\s*\n))*?LIFO'
flags: mi
---
