---
# The Schedule::new doc keeps why it checks at load.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'without[\s/]+re-checking'
---
