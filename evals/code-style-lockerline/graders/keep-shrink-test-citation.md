---
# Over-deletion. What the test's name does not say survives: the scan comes two minutes before the latch. The opening clause restates the test's name and may go.
type: regex
target: { source: file, path: tests/lockerline/LockerBankTest.java }
pattern: 'two\s+(?:(?:\*|//)\s*)?minutes'
flags: i
---
