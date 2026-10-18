---
# Over-deletion. The class summary says what no signature can, and cites its record, which src/ allows [claim + citation].
type: regex
target: { source: file, path: src/lockerline/StatusCodes.java }
pattern: 'never\s+(?:(?:\*|//)\s*)?renumber\s+(?:(?:\*|//)\s*)?one'
flags: i
---
