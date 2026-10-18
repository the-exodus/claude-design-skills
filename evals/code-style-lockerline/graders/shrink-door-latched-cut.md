---
# Under-deletion. The opening clause restates onDoorLatched.
type: regex
target: { source: file, path: src/lockerline/BankListener.java }
pattern: 'The\s+(?:(?:\*|//)\s*)?door\s+(?:(?:\*|//)\s*)?has\s+(?:(?:\*|//)\s*)?latched\s+(?:(?:\*|//)\s*)?and'
flags: i
match: not_contains
---
