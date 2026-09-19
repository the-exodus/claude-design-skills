---
# No component or function name anywhere in the written lexicon. Case-sensitive.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '\b(?:CatalogIndex|FineCalculator|HoldManager|LoanReconciler|NotificationQueue|LoanRepository|BranchSite|OverdueState|RequestContext)\b|renew\(\)'
match: not_contains
---
