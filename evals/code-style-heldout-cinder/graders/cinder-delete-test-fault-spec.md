---
# The controller test comment restating the abort rule from the decision record is gone.
type: regex
target: { source: file, path: tests/controller_test.rs }
pattern: 'starts[\s/]+the[\s/]+count[\s/]+again|third[\s/]+consecutive[\s/]+fault'
flags: i
match: not_contains
---
