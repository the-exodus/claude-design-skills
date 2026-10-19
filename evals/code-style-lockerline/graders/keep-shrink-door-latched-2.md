---
# Over-deletion. The contract survives the shrink.
type: regex
target: { source: file, path: src/lockerline/BankListener.java }
pattern: 'not\s+(?:(?:\*|//)\s*)?from\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?courier''s\s+(?:(?:\*|//)\s*)?scan'
flags: i
---
