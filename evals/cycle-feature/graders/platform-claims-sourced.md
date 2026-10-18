---
# Platform claims are marked documented, probed or recalled (THE-173).
type: regex
target: trace
pattern: '\b(?:[Dd]ocumented|[Pp]robed|[Rr]ecalled)\b[^\n]{0,80}monotonic|monotonic[^\n]{0,200}\b(?:documented|probed|recalled)\b'
---
