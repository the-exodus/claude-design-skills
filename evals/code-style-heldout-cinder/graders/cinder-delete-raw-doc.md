---
# The doc on QuarterDegrees::raw, a restatement of its name, is gone.
type: regex
target: { source: file, path: src/temperature.rs }
pattern: 'raw[\s/]+quarter-degree[\s/]+count'
flags: i
match: not_contains
---
