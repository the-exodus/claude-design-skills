---
# The cooling comment in run_window keeps its reason: the kiln sheds heat faster than any scheduled rate.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'sheds[\s/]+heat[\s/]+faster'
---
