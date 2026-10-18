---
# Over-deletion. What the fake does, beside the harness [fixture description].
type: regex
target: { source: file, path: tests/lockerline/FakeLockBoard.java }
pattern: 'as\s+(?:(?:\*|//)\s*)?the\s+(?:(?:\*|//)\s*)?real\s+(?:(?:\*|//)\s*)?sensor\s+(?:(?:\*|//)\s*)?does'
---
