---
# The 'below five, call the warehouse' sentence has no other home and is listed as such.
type: regex
target: last_message
pattern: '(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))[\s\S]{0,800}?(?:below five|call the warehouse)|(?:below five|call the warehouse)[^\n]{0,300}?(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))'
flags: i
---
