---
# The 56-to-60-days sentence has no other home and is listed as such.
type: regex
target: last_message
pattern: '(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))[\s\S]{0,800}?(?:release 2\.3|56 days|dry cow tubes|raised to 60)|(?:release 2\.3|56 days|dry cow tubes|raised to 60)[^\n]{0,300}?(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))'
flags: i
---
