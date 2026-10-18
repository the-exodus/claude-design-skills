---
# The MIN_ON doc keeps the zero-crossing relay and half-cycle reasoning.
type: regex
target: { source: file, path: src/relay.rs }
pattern: 'zero.crossing[\s\S]*half.cycle'
flags: i
---
