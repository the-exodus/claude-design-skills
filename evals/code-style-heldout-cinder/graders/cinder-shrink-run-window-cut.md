---
# The run_window doc no longer narrates the body: reads, sets, sleeps.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'reads[\s/]+the[\s/]+thermocouple,|sleeps[\s/]+until[\s/]+the[\s/]+window[\s/]+ends'
flags: i
match: not_contains
---
