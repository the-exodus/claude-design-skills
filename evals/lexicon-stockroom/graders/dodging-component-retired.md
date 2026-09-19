---
# StockLot exists to dodge the domain word batch.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:StockLot)\*\*'
flags: mi
match: not_contains
---
