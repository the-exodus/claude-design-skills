---
# The architecture relay rule keeps its claim and its citation of 0002.
type: regex
target: { source: file, path: tests/architecture/layering.rs }
pattern: 'except[\s/]+through[\s/]+`?Relay`?[\s/]*\(0002\)'
---
