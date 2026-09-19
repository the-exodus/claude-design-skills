---
# Drift: 'applied only once ... ever' is contradicted by RuleTrigger.TitleChange, so the lexicon stops asserting it.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: 'only once|ever triggers a rule again'
flags: i
match: not_contains
---
