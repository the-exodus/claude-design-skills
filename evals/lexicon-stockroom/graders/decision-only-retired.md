---
# The phrase exists only in the glossary; the content is ADR-0004's.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:two-phase pick)\*\*'
flags: mi
match: not_contains
---
