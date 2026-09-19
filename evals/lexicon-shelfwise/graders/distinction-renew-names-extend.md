---
# The distinction survives: each entry names the other. Also the Renewal DTO decoy.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:renew)\*\*(?:[^\n]|\n(?!\s*\n))*?\bextend'
flags: mi
---
