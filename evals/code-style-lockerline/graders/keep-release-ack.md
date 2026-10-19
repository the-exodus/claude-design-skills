---
# Over-deletion. The board answers before the solenoid moves [platform fact].
type: regex
target: { source: file, path: src/lockerline/LockBoard.java }
pattern: 'ACK\s+(?:(?:\*|//)\s*)?before\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?solenoid'
flags: i
---
