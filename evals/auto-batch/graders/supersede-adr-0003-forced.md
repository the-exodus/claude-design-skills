---
# Superseding ADR-0003 is a provisional item marked forced.
type: regex
target: { source: file, path: batch.md }
pattern: '^(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S])*?\bP\d\b(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S])*?(?:ADR-?0003(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S]){0,600}?\bforced\b|\bforced\b(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S]){0,300}?ADR-?0003)'
flags: i
---
