---
# Fixed: the hold fee uses integer arithmetic (ADR-0002).
type: regex
target: { source: file, path: ferrybook/pricing.py }
pattern: 'fare \* 0\.1'
match: not_contains
---
