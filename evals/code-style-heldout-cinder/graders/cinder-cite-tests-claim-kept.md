---
# The general test comment keeps its own claim once the citation goes.
type: regex
target: { source: file, path: tests/schedule_test.rs }
pattern: 'would[\s/]+panic'
---
