---
# The old row keeps its status and adds the partial supersede. The pointer may be plain text or a link.
type: regex
target: { source: file, path: docs/adr/README.md }
pattern: '\[0001\]\([^)]*\)[^\n]*\|\s*Accepted;\s*partly superseded by[^|\n]*0005'
flags: i
---
