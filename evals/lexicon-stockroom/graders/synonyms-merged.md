---
# Test 3: item code is SKU, stock is on-hand; shelf is retired or merged into bin.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:item code|stock|shelf)\*\*'
flags: mi
match: not_contains
---
