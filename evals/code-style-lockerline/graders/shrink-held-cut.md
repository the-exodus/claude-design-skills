---
# Under-deletion. The re-listing of the other codes duplicates their definitions and rots.
type: regex
target: { source: file, path: src/lockerline/StatusCodes.java }
pattern: '5\s+(?:(?:\*|//)\s*)?\(fault\)'
flags: i
match: not_contains
---
