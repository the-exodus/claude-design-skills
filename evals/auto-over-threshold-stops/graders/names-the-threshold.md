---
# It says the batch would exceed the threshold of five items: "threshold", "capped at five", "at most five", "more than five", "a limit of five".
type: regex
target: last_message
pattern: 'threshold|\bcap(?:s|ped)?\b[^\n]{0,60}(?:five|5\b)|at most (?:five|5\b)|(?:more than|over|exceed\w*|above|beyond|past)\s+(?:the\s+)?(?:limit|cap|five|5\b)|(?:limit|maximum|max) (?:of|is) (?:five|5\b)|(?:five|5)[- ](?:item|question)s? (?:limit|cap|maximum)'
flags: i
---
