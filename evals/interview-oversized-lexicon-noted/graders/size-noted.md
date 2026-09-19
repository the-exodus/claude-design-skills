---
# It says the lexicon is past about thirty entries, or counts them.
type: regex
target: last_message
pattern: '(?:\b3[0-9]\b|\bthirty(?:-\w+)?\b)[^\n]{0,160}\b(?:entr|term)|\b(?:entr|term)\w*[^\n]{0,160}(?:\b3[0-9]\b|\bthirty)|past (?:the|its) (?:size|limit)|over(?: the)? (?:size )?limit'
flags: i
---
