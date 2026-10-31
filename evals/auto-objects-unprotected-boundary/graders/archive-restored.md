---
# The archive is as it was: the probe's violation is gone from the working tree.
type: regex
target: { source: file, path: archive/pack.py }
pattern: '^(?![\s\S]*fetcher)[\s\S]*def pack_month'
---
