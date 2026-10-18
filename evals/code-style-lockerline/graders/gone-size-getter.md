---
# Under-deletion. Restates size() [pure restatement].
type: regex
target: { source: file, path: src/lockerline/Compartment.java }
pattern: 'Returns\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?compartment''s\s+(?:(?:\*|//)\s*)?size'
match: not_contains
---
