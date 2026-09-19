---
# Test 1: component names are not entries.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:CatalogIndex|FineCalculator|HoldManager|LoanReconciler|NotificationQueue|repository layer)\*\*'
flags: mi
match: not_contains
---
