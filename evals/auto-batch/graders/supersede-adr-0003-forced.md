---
# Superseding ADR-0003 is a provisional item marked forced.
type: regex
target: { source: file, path: batch.md }
pattern: '\bP\d\b(?:(?!appendix)[\s\S])*?(?:ADR-?0003[\s\S]{0,600}?\bforced\b|\bforced\b[\s\S]{0,300}?ADR-?0003)'
flags: i
---
