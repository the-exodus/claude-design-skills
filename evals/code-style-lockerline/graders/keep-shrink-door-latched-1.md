---
# Over-deletion. The contract survives the shrink.
type: regex
target: { source: file, path: src/lockerline/BankListener.java }
pattern: 'debounce\s+(?:(?:\*|//)\s*)?has\s+(?:(?:\*|//)\s*)?run'
---
