---
# Over-deletion. Looks like it restates the 3, but is the only record of why it is 3 [trap].
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: 'as\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?printed\s+(?:(?:\*|//)\s*)?receipt\s+(?:(?:\*|//)\s*)?promises'
flags: i
---
