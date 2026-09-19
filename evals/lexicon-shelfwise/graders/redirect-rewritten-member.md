---
# Decoy: the 'See patron' stub hides a distinct concept. Kept, no longer a redirect, names patron.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*member\*\*(?![\s—–:-]*see\b)(?:[^\n]|\n(?!\s*\n))*?\bpatron'
flags: mi
---
