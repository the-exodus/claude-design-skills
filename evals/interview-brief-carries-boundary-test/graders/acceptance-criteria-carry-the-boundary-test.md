---
# The acceptance criteria, which the template writes last, name the architecture test that protects U1's boundary.
type: regex
target: { source: file, path: docs/brief-silent-stations.md }
pattern: '^#+[^\n]*Acceptance criteria[\s\S]*(?:architecture test|test_architecture)'
flags: im
---
