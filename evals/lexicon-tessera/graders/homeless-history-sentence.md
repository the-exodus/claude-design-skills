---
# The columns-until-0.4 sentence has no other home and is listed as such.
type: regex
target: last_message
pattern: '(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))[\s\S]{0,800}?(?:ultrawide|\b0\.4\b|off-cent|columns until|was columns)|(?:ultrawide|\b0\.4\b|off-cent|columns until|was columns)[^\n]{0,300}?(?:homeless|no (?:other )?home|nowhere else|lives nowhere|not (?:recorded|stated|found) (?:anywhere|elsewhere))'
flags: i
---
