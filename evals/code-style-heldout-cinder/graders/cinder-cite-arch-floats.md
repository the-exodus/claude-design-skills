---
# The architecture float rule keeps its claim and its citation of 0001.
type: regex
target: { source: file, path: tests/architecture/layering.rs }
pattern: 'cross[\s/]+module[\s/]+boundaries[\s\S]{0,80}\(0001\)'
---
