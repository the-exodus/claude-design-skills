---
# Under-deletion. A specification restated in a test file; under tests/ no pointer may replace it either.
type: regex
target: { source: file, path: tests/lockerline/LockerBankTest.java }
pattern: 'lock\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?compartment\s+(?:(?:\*|//)\s*)?out\s+(?:(?:\*|//)\s*)?until\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?next\s+(?:(?:\*|//)\s*)?courier\s+(?:(?:\*|//)\s*)?round'
flags: i
match: not_contains
---
