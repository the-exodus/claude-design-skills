---
# Under-deletion. Restates the next line.
type: regex
target: { source: file, path: tests/lockerline/LockerBankTest.java }
pattern: 'Arrange\s+(?:(?:\*|//)\s*)?a\s+(?:(?:\*|//)\s*)?bank'
match: not_contains
---
