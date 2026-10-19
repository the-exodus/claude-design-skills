---
# The pointer-only doc on WINDOW (See 0002.) is gone.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'See[\s/]+0002'
flags: i
match: not_contains
---
