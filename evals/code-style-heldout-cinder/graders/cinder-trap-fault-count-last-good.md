---
# The take_reading doc keeps what a fault short of the third reports.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'last[\s/]+good[\s/]+temperature'
---
