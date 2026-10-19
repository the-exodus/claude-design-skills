---
# The decode doc keeps the MAX31855 frame layout: temperature in bits 31..18, fault flag in bit 16.
type: regex
target: { source: file, path: src/thermocouple.rs }
pattern: 'bits[\s/]+31\.\.18[\s\S]*bit[\s/]+16'
flags: i
---
