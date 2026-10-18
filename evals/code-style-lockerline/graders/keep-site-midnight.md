---
# Over-deletion. The instant is 23:59:59 at the site [non-local: the zone].
type: regex
target: { source: file, path: tests/lockerline/DwellPolicyTest.java }
pattern: '23:59:59\s+(?:(?:\*|//)\s*)?at\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?site'
---
