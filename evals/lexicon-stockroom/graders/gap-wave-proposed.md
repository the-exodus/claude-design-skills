---
# The gap: wave is used everywhere and never defined. The file has no gaps line, so it is presented in the report, under a gaps heading, under one that calls the words proposed, or as a word said to have no definition.
type: regex
target: last_message
pattern: '(?:\bgaps?\b|\bproposed\b)[\s\S]{0,1200}?\bwave\b|\bwave\b[^\n]{0,300}?(?:never defined|not defined|undefined|without a definition|no definition)'
flags: i
---
