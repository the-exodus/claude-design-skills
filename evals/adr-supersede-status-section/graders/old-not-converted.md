---
# Old ADRs are not converted to the house format: no **Status:** line is added where the ADR had its own field.
type: regex
target: { source: file, path: docs/adr/0002-poll-gauges-every-five-minutes.md }
pattern: '\*\*Status:\*\*'
match: not_contains
---
