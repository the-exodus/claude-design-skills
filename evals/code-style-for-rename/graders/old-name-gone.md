---
# Everywhere it appears.
type: regex
target: { source: file, path: gaugefeed/fetcher.py }
pattern: 'fetch_all'
match: not_contains
---
