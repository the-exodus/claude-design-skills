---
# Over-deletion. The reason survives the shrink.
type: regex
target: { source: file, path: src/lockerline/StatusCodes.java }
pattern: 'tell\s+(?:(?:\*|//)\s*)?an\s+(?:(?:\*|//)\s*)?inspection'
---
