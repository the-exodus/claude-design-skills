---
# The index row for 0001 points at both successors.
type: regex
target: { source: file, path: docs/adr/README.md }
pattern: '\[0001\]\([^)]*\)[^\n]*Superseded by[^|\n]*000[56][^|\n]*000[56]'
---
