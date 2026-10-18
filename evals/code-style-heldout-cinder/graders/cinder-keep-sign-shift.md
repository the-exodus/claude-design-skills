---
# The comment on the i32 shift keeps why: the arithmetic shift carries the sign bit.
type: regex
target: { source: file, path: src/thermocouple.rs }
pattern: 'sign[\s/]+bit'
---
