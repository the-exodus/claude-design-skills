---
# Drift at a known line: enum OverdueState at src/loans/fines.ts:6-13, or the uses at :26, :28, :43.
type: regex
target: last_message
pattern: 'fines\.ts[^\n\w]{0,4}(?:lines?\s*|L)?(?:[5-9]|1[0-3]|26|28|43)\b'
---
