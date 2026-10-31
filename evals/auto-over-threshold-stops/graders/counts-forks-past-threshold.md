---
# The handed-over tree carries the counts line with more than five genuine forks, which any stop under the amended decision D needs.
type: regex
target: { source: file, path: batch.md }
pattern: 'Forks:\W*(?:[6-9]|\d{2,})\s+genuine,\s*\d+\s+decided'
flags: i
---
