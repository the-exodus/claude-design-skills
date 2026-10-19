---
# Over-deletion. The constant-time contract and its reason survive.
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: 'time\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?scanner''s\s+(?:(?:\*|//)\s*)?beep'
flags: i
---
