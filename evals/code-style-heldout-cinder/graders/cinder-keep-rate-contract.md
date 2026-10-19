---
# The rate_per_hour doc keeps its unit and that Schedule::new checks the sign rules.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'quarter-degrees[\s/]+per[\s/]+hour[\s\S]*Schedule::new`?[\s/]+checks'
flags: i
---
