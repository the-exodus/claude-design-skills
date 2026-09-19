---
# Rows are never deleted.
type: regex
target: { source: file, path: docs/adr/README.md }
pattern: '^(?=[\s\S]*\[0001\]\()(?=[\s\S]*\[0002\]\()(?=[\s\S]*\[0004\]\()'
---
