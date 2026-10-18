---
# The comment's claim that an unweighed roast is left off the report is false after the change, and does not survive.
type: regex
target: { source: file, path: roastlog/report.py }
pattern: 'left\s+off\s+(?:#\s*)?the\s+(?:#\s*)?report'
flags: i
match: not_contains
---
