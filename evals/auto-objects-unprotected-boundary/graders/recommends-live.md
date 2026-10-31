---
# It recommends a live interview: "run this live", "a live interview", "live mode".
type: regex
target: last_message
pattern: '\blive\b[^\n]{0,40}(?:mode|interview|session|design)|(?:\brun\w*|interview|design)[^\n]{0,40}\blive\b|interactive(?:ly)?[^\n]{0,20}(?:interview|session|mode)'
flags: i
---
