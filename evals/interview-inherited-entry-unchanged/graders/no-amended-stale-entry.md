---
# No rewritten stale entry is drafted: a bold headword and a dash followed by anything but the inherited text.
type: regex
target: last_message
pattern: '\*\*\*?stale\*?\*\*\s*[—–-]\s*(?!Said of a \*reading\* older than two \*cycles\*)'
flags: i
match: not_contains
---
