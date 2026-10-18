---
# The storage decision still stands, so the old ADR keeps its status and adds "partly superseded by" in the field it already has: a ## Status section.
type: regex
target: { source: file, path: docs/adr/0001-store-readings-in-sqlite-and-back-up-nightly.md }
pattern: '^## Status\s*\n+\s*Accepted\b[^\n]*partly superseded by \[ADR-0005\]\(0005-replicate-station-write-ahead-logs-continuously-to-object-storage\.md\)'
flags: mi
---
