---
# It says the genuine forks exceed the threshold: "threshold", "a third of the decided branches", "the floor", "capped at five", "at most five", "more than five".
type: regex
target: last_message
pattern: 'threshold|a third of|\bfloor\b|\bcap(?:s|ped)?\b[^\n]{0,60}(?:five|5\b)|at most (?:five|5\b)|(?:more than|over|exceed\w*|above|beyond|past)\s+(?:the\s+)?(?:limit|cap|five|5\b)|(?:limit|maximum|max) (?:of|is) (?:five|5\b)|(?:five|5)[- ](?:item|question)s? (?:limit|cap|maximum)'
flags: i
---
