---
# Over-deletion. How dwell is counted, with its record [claim + citation].
type: regex
target: { source: file, path: src/lockerline/DwellPolicy.java }
pattern: 'one\s+(?:(?:\*|//)\s*)?day\s+(?:(?:\*|//)\s*)?at\s+(?:(?:\*|//)\s*)?midnight'
flags: i
---
