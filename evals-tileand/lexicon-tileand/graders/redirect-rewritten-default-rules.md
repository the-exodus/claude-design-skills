---
# The 'See compat library' stub hides a distinct concept: the defaults are baked in, the compat library is applied on top. This checks only that the concept has a real entry. The headword is not graded (the owner marked the row unsure on 2026-09-20: the docs say 'shipped defaults', the code and the log say 'shipped rule'), so any of the three passes.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:default rules|shipped defaults|shipped rules)\*\*(?![\s—–:-]*see\b)'
flags: mi
---
