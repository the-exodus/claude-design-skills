---
# No component or function name anywhere in the written glossary. StockLot may be noted as the code's word for batch. Case-sensitive.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '\b(?:AllocationEngine|CollectionDesk|PickListBuilder|ReservationService|SkuCache)\b|available_qty|\buow\('
match: not_contains
---
