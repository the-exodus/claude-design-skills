---
# Decoy: the 'See floating window' stub hides a distinct concept (float vs ignore).
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\*\*unmanaged window\*\*(?![\s—–:-]*see\b)'
flags: mi
---
