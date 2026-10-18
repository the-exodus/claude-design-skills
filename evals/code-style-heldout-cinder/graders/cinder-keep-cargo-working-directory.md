---
# The architecture helper keeps that cargo runs integration tests from the crate root.
type: regex
target: { source: file, path: tests/architecture/main.rs }
pattern: 'working[\s/]+directory'
---
