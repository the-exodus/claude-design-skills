---
# Over-deletion. In tests/architecture/ a citation beside the comment's own words is allowed [claim + citation].
type: regex
target: { source: file, path: tests/architecture/ControllerIsolationTest.java }
pattern: 'ADR\-0001'
flags: i
---
