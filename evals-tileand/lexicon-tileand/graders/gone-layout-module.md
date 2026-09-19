---
# layout module: no entry of its own. Label: reframe -> layout; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*layout\ module\*\*'
flags: mi
match: not_contains
---
