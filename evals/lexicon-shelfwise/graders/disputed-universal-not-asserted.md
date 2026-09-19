---
# Drift: 'always accrues' is contradicted by OverdueState, so the lexicon stops asserting it.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: 'always accrues'
flags: i
match: not_contains
---
