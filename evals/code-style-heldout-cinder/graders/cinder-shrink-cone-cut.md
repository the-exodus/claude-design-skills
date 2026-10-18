---
# The Cone doc no longer re-lists the variants.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: '06,[\s/]*04,[\s/]*5'
match: not_contains
---
