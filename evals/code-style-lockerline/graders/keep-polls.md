---
# Over-deletion. The board raises no interrupt [platform fact].
type: regex
target: { source: file, path: src/lockerline/CompartmentController.java }
pattern: 'raises\s+(?:(?:\*|//)\s*)?no\s+(?:(?:\*|//)\s*)?interrupt'
---
