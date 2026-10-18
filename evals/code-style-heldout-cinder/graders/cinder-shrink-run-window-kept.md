---
# The run_window doc keeps its caller contract about calling again at once.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'between[\s/]+calls[\s\S]*slow[\s/]+caller'
flags: i
---
