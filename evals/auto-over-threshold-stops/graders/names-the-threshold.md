---
# It says the batch would exceed the threshold of five items.
type: regex
target: last_message
pattern: 'threshold|(?:more than|over|exceed\w*|above|beyond|past)\s+(?:the\s+)?(?:limit|five|5\b)'
flags: i
---
