---
# Over-deletion. Which thread the bank's state changes on, and why listener calls are posted [contract].
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: 'never\s+(?:(?:\*|//)\s*)?on\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?lock\-board\s+(?:(?:\*|//)\s*)?thread'
---
