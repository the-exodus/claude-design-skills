---
# The header's standing exclusion of layout vocabulary goes, so master can be re-tested.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: 'Layout-specific vocabulary belongs to its layout module'
flags: i
match: not_contains
---
