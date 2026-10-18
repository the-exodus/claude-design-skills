---
# The glossary term Segment still names the schedule step struct.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'pub[\s/]+struct[\s/]+Segment[\s/]*\{'
---
