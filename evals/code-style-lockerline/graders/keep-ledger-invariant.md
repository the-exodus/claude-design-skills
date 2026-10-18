---
# Over-deletion. The one-reservation invariant is held by another class [invariant guarded elsewhere].
type: regex
target: { source: file, path: src/lockerline/LockerBank.java }
pattern: 'the\s+(?:(?:\*|//)\s*)?ledger''s\s+(?:(?:\*|//)\s*)?lock\s+(?:(?:\*|//)\s*)?holds\s+(?:(?:\*|//)\s*)?that'
flags: i
---
