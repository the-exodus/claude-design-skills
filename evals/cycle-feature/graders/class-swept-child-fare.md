---
# The class sweep found the same float pattern in child_fare, outside the change; minor and mechanical, so by the default policy it is fixed in the PR.
type: regex
target: { source: file, path: ferrybook/pricing.py }
pattern: '\* 0\.5'
match: not_contains
---
