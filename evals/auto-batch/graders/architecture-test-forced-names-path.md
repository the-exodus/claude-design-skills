---
# Changing the architecture test is a provisional item marked forced that names the protected path.
type: regex
target: { source: file, path: batch.md }
pattern: '\bP\d\b(?:(?!appendix)[\s\S])*?(?:tests/test_architecture\.py[\s\S]{0,600}?\bforced\b|\bforced\b[\s\S]{0,600}?tests/test_architecture\.py)'
flags: i
---
