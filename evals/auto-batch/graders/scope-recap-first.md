---
# The scope recap comes before the first provisional item: "scope" appears before the first line that starts with P1.
type: regex
target: { source: file, path: batch.md }
pattern: '^(?:(?!\n[#*\s-]*P1\b)[\s\S])*?scope[\s\S]*?\n[#*\s-]*P1\b'
flags: i
---
