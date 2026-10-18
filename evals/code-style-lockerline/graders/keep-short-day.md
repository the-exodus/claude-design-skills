---
# Over-deletion. The zone and its short day [non-local fact].
type: regex
target: { source: file, path: tests/lockerline/DwellPolicyTest.java }
pattern: '23\s+(?:(?:\*|//)\s*)?hours\s+(?:(?:\*|//)\s*)?long'
---
