---
# It proceeds past the suitability check (the archive is outside the blast radius) and writes a batch with provisional items.
type: regex
target: { source: file, path: batch.md }
pattern: '\bP1\b'
---
