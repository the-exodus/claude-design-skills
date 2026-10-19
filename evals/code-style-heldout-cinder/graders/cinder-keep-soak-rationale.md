---
# The soak-timing comment in run_window keeps its rationale.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'full[\s/]+soak'
---
