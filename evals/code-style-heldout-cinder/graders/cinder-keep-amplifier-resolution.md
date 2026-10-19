---
# The QuarterDegrees doc keeps the amplifier's 0.25 degree resolution.
type: regex
target: { source: file, path: src/temperature.rs }
pattern: 'resolves[\s/]+0\.25'
---
