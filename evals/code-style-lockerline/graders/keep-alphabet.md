---
# Over-deletion. Why these characters [rationale].
type: regex
target: { source: file, path: src/lockerline/CollectionCodes.java }
pattern: 'misread\s+(?:(?:\*|//)\s*)?on\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?thermal\s+(?:(?:\*|//)\s*)?receipt'
flags: i
---
