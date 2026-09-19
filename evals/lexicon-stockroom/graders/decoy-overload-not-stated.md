---
# An overload that doesn't count: nobody confuses a customer return with a return value. Passes if return is retired.
type: regex
target: { source: file, path: GLOSSARY.md }
pattern: '^\*\*(?:return)\*\*(?:[^\n]|\n(?!\s*\n))*?(?:return value|function|statement|keyword)'
flags: mi
match: not_contains
---
