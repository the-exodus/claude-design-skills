---
# Test 1: component names are not entries. GroupManager is the component beside the concept management group.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: '^\*\*(?:HerdStore|ListBuilder|MeterIngest|GroupManager)\*\*'
flags: mi
match: not_contains
---
