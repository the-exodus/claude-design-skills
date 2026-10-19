---
# Over-deletion. The contract survives the shrink.
type: regex
target: { source: file, path: src/lockerline/BankListener.java }
pattern: 'lock\-board\s+(?:(?:\*|//)\s*)?thread'
flags: i
---
