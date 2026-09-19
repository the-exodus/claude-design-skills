---
# session-end show: no entry of its own. Label: retire (folded into session end); the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*session\-end\ show\*\*'
flags: mi
match: not_contains
---
