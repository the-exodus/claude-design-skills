---
# An overload that counts: the pick queue is not FIFO and not the job queue.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:pick queue)\*\*(?:[^\n]|\n(?!\s*\n))*?(?:FIFO|first[- ]in)'
flags: mi
---
