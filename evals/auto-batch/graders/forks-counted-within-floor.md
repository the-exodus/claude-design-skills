---
# The batch carries the counts line, and the genuine forks are within the floor of five (decision D as amended 2026-10-31: forced items do not count).
type: regex
target: { source: file, path: batch.md }
pattern: 'Forks:\W*[0-5]\s+genuine,\s*\d+\s+decided'
flags: i
---
