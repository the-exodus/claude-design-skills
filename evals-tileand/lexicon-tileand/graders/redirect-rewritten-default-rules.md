---
# The 'See compat library' stub hides a distinct concept: the defaults are baked in, the compat library is applied on top. This checks only that the concept has a real entry, under either headword; the headword itself is the label's business (gone-default-rules, reframed-shipped-defaults), so a run that writes the entry but keeps the old word fails those and not this.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\*\*(?:default rules|shipped defaults)\*\*(?![\s—–:-]*see\b)'
flags: mi
---
