---
# The gap: the Insemination type dodges the undefined domain word service. The file has a Gaps line, so it goes there: anywhere in the header, above the horizontal rule.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\W{0,3}Gaps\b(?:(?!\n-{3})[\s\S]){0,800}?\bservice\b'
flags: mi
---
