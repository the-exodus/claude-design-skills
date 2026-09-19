---
# The old ADR keeps its body exactly as written.
type: regex
target: { source: file, path: docs/adr/0001-store-readings-in-sqlite-and-back-up-nightly.md }
pattern: '^(?=[\s\S]*\*\*Storage\.\*\* Each station''s readings live in their own SQLite file)(?=[\s\S]*\*\*Backups\.\*\* Every night at 02:00 each station file is copied)(?=[\s\S]*A disk failure loses at most one day of readings\.)'
---
