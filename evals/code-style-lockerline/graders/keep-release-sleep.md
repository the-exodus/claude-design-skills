---
# Over-deletion. The 40 ms wait has its reason only in this comment [rationale for a non-obvious line].
type: regex
target: { source: file, path: src/lockerline/CompartmentController.java }
pattern: 'within\s+(?:(?:\*|//)\s*)?30\s+(?:(?:\*|//)\s*)?ms'
flags: i
---
