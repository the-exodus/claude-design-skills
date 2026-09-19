---
# The owner's label: role needed a rewrite. Fails while the old text stands word for word.
type: regex
target: { source: file, path: docs/design/lexicon.md }
pattern: 'What a known window is: a \*root\*, a \*satellite\*, or a promoted root\.\s+Derived from\s+the Win32 owner relation\.\s+Distinct from \*membership\*\.'
flags: mi
match: not_contains
---
