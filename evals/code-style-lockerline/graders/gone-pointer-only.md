---
# Under-deletion. A comment that only points at a record; a citation never stands in for a claim.
type: regex
target: { source: file, path: src/lockerline/CollectionCodes.java }
pattern: 'See\s+(?:(?:\*|//)\s*)?ADR\-0003'
flags: i
match: not_contains
---
