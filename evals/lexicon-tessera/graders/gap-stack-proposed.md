---
# The gap: SecondaryArea dodges the undefined domain word stack. The file has a Gaps line, so it goes there: anywhere in the header, above the horizontal rule.
type: regex
target: { source: file, path: docs/lexicon.md }
pattern: '^\W{0,3}Gaps\b(?:(?!\n-{3})[\s\S]){0,800}?\bstack\b'
flags: mi
---
