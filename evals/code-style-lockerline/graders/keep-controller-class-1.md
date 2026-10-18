---
# Over-deletion. The controller's thread and the decision it holds to [contract + citation].
type: regex
target: { source: file, path: src/lockerline/CompartmentController.java }
pattern: 'lock\s+(?:(?:\*|//)\s*)?board''s\s+(?:(?:\*|//)\s*)?own\s+(?:(?:\*|//)\s*)?thread'
---
