---
# Over-deletion. Why the lock is held across both steps [rationale].
type: regex
target: { source: file, path: src/lockerline/ReservationLedger.java }
pattern: 'normal\s+(?:(?:\*|//)\s*)?case\s+(?:(?:\*|//)\s*)?at\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?depot\s+(?:(?:\*|//)\s*)?bank'
flags: i
---
