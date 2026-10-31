---
# Keeping timestamps in UTC draws no boundary, so the record makes no claim that one is enforced.
type: regex
target: { source: file, path: docs/adr/0005-keep-timestamps-in-utc-and-convert-only-when-rendering.md }
pattern: 'enforce this boundary'
flags: i
match: not_contains
---
