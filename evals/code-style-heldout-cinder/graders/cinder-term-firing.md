---
# The glossary term Firing still names the controller's struct.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'pub[\s/]+struct[\s/]+Firing<'
---
