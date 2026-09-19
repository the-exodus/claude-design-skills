---
# Changing a Status updates the index in the same change.
type: regex
target: { source: file, path: docs/adr/README.md }
pattern: '\[0002\]\([^)]*\)[^\n]*Superseded by ADR-0005'
---
