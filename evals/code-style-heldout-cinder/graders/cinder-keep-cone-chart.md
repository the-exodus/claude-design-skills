---
# The Cone::peak doc keeps where the peaks come from.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'cone[\s/]+maker'
flags: i
---
