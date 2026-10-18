---
# Under-deletion. The opening clause restates onCodeScanned.
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: 'A\s+(?:(?:\*|//)\s*)?collection\s+(?:(?:\*|//)\s*)?code\s+(?:(?:\*|//)\s*)?was\s+(?:(?:\*|//)\s*)?scanned\s+(?:(?:\*|//)\s*)?at\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?bank'
match: not_contains
---
