---
# emergency show: no entry of its own. Label: reframe -> rescue; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*emergency\ show\*\*'
flags: mi
match: not_contains
---
