---
# D3: next_free_slot builds the window in UTC, not site time (ADR 0001); wrong under the shipped Europe/London.
type: regex
target: last_message
pattern: 'timezone\.utc|BST|Europe/London|site_timezone|site time|local time'
flags: i
---
