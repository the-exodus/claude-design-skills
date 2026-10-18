---
# D8: the CLI cancels the blast at the postponement limit, which the brief did not ask for.
type: regex
target: last_message
pattern: 'PostponeLimitError|auto-?cancel|cancels the blast'
flags: i
---
