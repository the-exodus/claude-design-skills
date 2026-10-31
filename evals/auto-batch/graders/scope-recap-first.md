---
# The scope recap comes before the first provisional item.
type: regex
target: { source: file, path: batch.md }
pattern: '^(?:(?!\bP1\b)[\s\S])*?scope[\s\S]*?\bP1\b'
flags: i
---
