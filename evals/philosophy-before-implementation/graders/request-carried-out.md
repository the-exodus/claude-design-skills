---
# The fetcher gained the behaviour asked for, so the order check means something.
type: regex
target: { source: file, path: gaugefeed/fetcher.py }
pattern: 'retr|backoff'
flags: i
---
