---
# The Thermocouple::read doc keeps the chip's conversion time.
type: regex
target: { source: file, path: src/thermocouple.rs }
pattern: '100[\s/]*ms'
---
