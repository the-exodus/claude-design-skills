---
# The project's convention bars citations in tests, though ADR-0002 records the rule under test.
type: regex
target: { source: file, path: tests/test_development_ratio.py }
pattern: 'ADR|docs/adr|decision record'
flags: i
match: not_contains
---
