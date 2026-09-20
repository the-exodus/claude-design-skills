---
# Test 1: component names are not entries.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:AllocationEngine|CollectionDesk|event bus|ORM session|PickListBuilder|ReservationService|SkuCache)\*\*'
flags: mi
match: not_contains
---
