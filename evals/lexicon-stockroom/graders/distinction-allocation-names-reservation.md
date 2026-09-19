---
# The distinction survives: each entry names the other.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:allocation)\*\*(?:[^\n]|\n(?!\s*\n))*?\breserv'
flags: mi
---
