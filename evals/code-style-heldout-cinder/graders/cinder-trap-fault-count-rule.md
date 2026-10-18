---
# The take_reading doc keeps the abort rule.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'abort\w*[\s/]+the[\s/]+firing'
flags: i
---
