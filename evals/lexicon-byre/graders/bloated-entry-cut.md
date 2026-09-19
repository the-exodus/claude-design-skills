---
# The history of the default, and the config key, are not meaning.
type: regex
target: { source: file, path: docs/glossary.md }
pattern: 'release 2\.3|dry cow tubes|dry_period_days'
flags: i
match: not_contains
---
