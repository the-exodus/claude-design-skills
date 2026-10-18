---
# Under-deletion. The opening clause restates FanOutListener and its constructor.
type: regex
target: { source: file, path: src/lockerline/FanOutListener.java }
pattern: 'Forwards\s+(?:(?:\*|//)\s*)?each\s+(?:(?:\*|//)\s*)?event\s+(?:(?:\*|//)\s*)?to\s+(?:(?:\*|//)\s*)?several\s+(?:(?:\*|//)\s*)?listeners'
flags: i
match: not_contains
---
