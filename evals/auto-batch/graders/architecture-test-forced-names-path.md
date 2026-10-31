---
# Changing the architecture test is a provisional item marked forced that names the protected path.
type: regex
target: { source: file, path: batch.md }
pattern: '^(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S])*?\bP\d\b(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S])*?(?:tests/test_architecture\.py(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S]){0,600}?\bforced\b|\bforced\b(?:(?!\n[#*\d.\s:\u2014\u2013-]*appendix)[\s\S]){0,600}?tests/test_architecture\.py)'
flags: i
---
