---
# The comment in Firing::new keeps the invariant Schedule::new guards.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'rejects[\s/]+an[\s/]+empty[\s/]+schedule'
---
