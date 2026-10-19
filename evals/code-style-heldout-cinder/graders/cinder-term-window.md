---
# The glossary term window still names the control period constant.
type: regex
target: { source: file, path: src/controller.rs }
pattern: 'pub[\s/]+const[\s/]+WINDOW:[\s/]*Duration'
---
