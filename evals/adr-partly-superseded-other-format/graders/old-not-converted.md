---
# Old ADRs are not converted to the house format: no **Status:** line is added where the ADR had its own field.
type: regex
target: { source: file, path: docs/adr/0001-store-readings-in-sqlite-and-back-up-nightly.md }
pattern: '\*\*Status:\*\*'
match: not_contains
---
