---
# The distinction survives and becomes two-sided: the original milking entry does not name session.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:milking)\*\*(?:[^\n]|\n(?!\s*\n))*?\bsession'
flags: mi
---
