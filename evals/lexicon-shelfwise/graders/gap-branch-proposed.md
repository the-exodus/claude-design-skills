---
# The gap: BranchSite dodges the undefined domain word branch. The file has a Gaps line, so it goes there: anywhere in the header, before the --- rule.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^\W{0,3}Gaps\b(?:(?!\n---)[\s\S]){0,800}?\bbranch\b'
flags: mi
---
