---
# The glossary term soak still names the Segment field.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'pub[\s/]+soak:[\s/]*Duration'
---
