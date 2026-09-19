---
# No source says 'despatch note'. True whether the run renames it to packing slip or retires it.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:despatch note)\*\*'
flags: mi
match: not_contains
---
