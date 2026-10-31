---
# It recommends a live interview.
type: regex
target: last_message
pattern: '\blive\b[^\n]{0,40}(?:mode|interview|session|design)|interactive(?:ly)?[^\n]{0,20}(?:interview|session|mode)'
flags: i
---
