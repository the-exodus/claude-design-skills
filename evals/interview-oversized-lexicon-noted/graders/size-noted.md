---
# It says the lexicon is past about thirty entries, or counts them. Any count from thirty up passes: one run called the 34 entries forty-odd.
type: regex
target: last_message
pattern: '(?:\b[3-9][0-9]\b|\b(?:thirty|forty)(?:-\w+)?\b)[^\n]{0,160}\b(?:entr|term)|\b(?:entr|term)\w*[^\n]{0,160}(?:\b[3-9][0-9]\b|\bthirty|\bforty)|past (?:the|its) (?:useful )?(?:size|limit)|over(?: the)? (?:size )?limit'
flags: i
---
