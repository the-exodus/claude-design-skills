---
# Over-deletion. Why the count is one [rationale].
type: regex
target: { source: file, path: tests/lockerline/LockerBankTest.java }
pattern: 'no\s+(?:(?:\*|//)\s*)?scan\s+(?:(?:\*|//)\s*)?opened\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?door'
---
