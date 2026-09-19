---
# The distinction survives: each entry names the other.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:reservation)\*\*(?:[^\n]|\n(?!\s*\n))*?\ballocat'
flags: mi
---
