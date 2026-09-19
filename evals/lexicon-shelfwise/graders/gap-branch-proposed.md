---
# The gap: BranchSite dodges the undefined domain word branch. The file has a Gaps line, so it goes there.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: '^Gaps:(?:[^\n]|\n(?!\s*\n))*?\bbranch\b'
flags: mi
---
