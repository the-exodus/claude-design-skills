---
# ADRs in another format get no edit beyond their status.
type: regex
target: { source: file, path: docs/adr/0001-store-readings-in-sqlite-and-back-up-nightly.md }
pattern: '^#+\s*Addendum\b'
flags: mi
match: not_contains
---
