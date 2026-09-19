---
# The 'See compat library' stub hides a distinct concept: the defaults are baked in, the compat library is applied on top. Passes under either headword, since the sources say 'shipped defaults'; kept-default-rules checks the headword.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:default rules|shipped defaults)\*\*(?![\s—–:-]*see\b)'
flags: mi
---
