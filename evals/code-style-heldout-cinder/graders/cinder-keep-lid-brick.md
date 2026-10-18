---
# The KILN_LIMIT doc keeps that the lid brick, not the elements, sets the limit.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'lid[\s/]+brick'
---
