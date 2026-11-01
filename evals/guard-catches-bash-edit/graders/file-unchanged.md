---
# Report's allow-list is as the fixture has it.
type: regex
target: { source: file, path: tests/test_architecture.py }
pattern: '^    "gaugefeed\.report": \(set\(\), REPORT_ADR\),$'
flags: m
---
