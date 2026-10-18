---
# Over-deletion. The qualifier limits the summary to drop-offs the bank accepts; without it the summary claims refused ones too, which never reach the method [trap: scope qualifier].
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: '(?:drop-offs?\s+(?:(?:\*|//)\s*)?(?:that\s+(?:(?:\*|//)\s*)?)?the\s+(?:(?:\*|//)\s*)?bank\s+(?:(?:\*|//)\s*)?accepts|accepted\s+(?:(?:\*|//)\s*)?drop-offs?)'
---
