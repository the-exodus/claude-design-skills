---
# The Cone doc keeps why cones are an enum.
type: regex
target: { source: file, path: src/schedule.rs }
pattern: 'known[\s/]+peak[\s\S]*fails[\s/]+to[\s/]+compile'
flags: i
---
