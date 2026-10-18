---
# Over-deletion. In tests/architecture/ a citation beside the comment's own words is allowed [claim + citation].
type: regex
target: { source: file, path: tests/architecture/ControllerIsolationTest.java }
pattern: 'through\s+(?:(?:\*|//)\s*)?reflection\s+(?:(?:\*|//)\s*)?is\s+(?:(?:\*|//)\s*)?not\s+(?:(?:\*|//)\s*)?seen'
---
