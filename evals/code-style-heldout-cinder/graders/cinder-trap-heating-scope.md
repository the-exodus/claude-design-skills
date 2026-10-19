---
# The planned_duration doc keeps its scope qualifier: heating segments only.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'heating[\s/]+segments'
flags: i
---
