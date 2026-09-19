---
# desired state: still an entry. Label: rewrite; the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*desired\ state\*\*'
flags: mi
---
