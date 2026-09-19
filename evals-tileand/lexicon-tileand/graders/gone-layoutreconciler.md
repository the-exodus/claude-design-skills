---
# LayoutReconciler: no entry of its own. Label: reframe -> reconcile; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*LayoutReconciler\*\*'
flags: mi
match: not_contains
---
