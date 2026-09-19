---
# Decoy: the 'See cow' stub hides a distinct concept the code and docs distinguish everywhere.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*heifer\*\*(?![\s—–:-]*see\b)'
flags: mi
---
