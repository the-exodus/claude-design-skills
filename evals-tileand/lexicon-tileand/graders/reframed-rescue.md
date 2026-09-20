---
# emergency show becomes what a user observes. The owner: 'rescue' is simply a better pick. Any of rescue, rescued and rescued end passes (the owner, 2026-09-20: accept rescued end, which a run wrote for the same concept).
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*rescued?(?: end)?\*\*'
flags: mi
---
