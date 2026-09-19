---
# default rules: still an entry. Label: rewrite (the redirect becomes a real entry); the owner's label.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*default\ rules\*\*'
flags: mi
---
