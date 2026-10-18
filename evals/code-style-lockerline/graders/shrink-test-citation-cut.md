---
# Under-deletion. Under tests/ the claim stays and its citation goes.
type: regex
target: { source: file, path: tests/lockerline/LockerBankTest.java }
pattern: 'ADR\-'
match: not_contains
---
