---
# Trap: without the quarantine exception, 'on-hand less reserved' is a false universal.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:available)\*\*(?:[^\n]|\n(?!\s*\n))*?quarantin'
flags: mi
---
