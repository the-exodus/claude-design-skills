---
# Decoy: the 'See reservation' stub hides a distinct concept.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*backorder\*\*(?![\s—–:-]*see\b)'
flags: mi
---
