---
# Changing a Status updates the index in the same change. The pointer may be plain text or a link.
type: regex
target: { source: file, path: docs/adr/README.md }
pattern: '\[0002\]\([^)]*\)[^\n]*Superseded by[^|\n]*0005'
---
