---
# The change was made: the loop no longer skips a roast with no roasted weight.
type: regex
target: { source: file, path: roastlog/report.py }
pattern: 'roasted_weight_g\s+is\s+None:\s*\n\s*continue'
match: not_contains
---
