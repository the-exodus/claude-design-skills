---
# D1: _new_ref reuses a settled hold's reference, against ADR-0001. A correct report may name the function, quote its max(...), say in words that references are reused, reissued or issued again, or say that ADR-0001 is broken: that record decides nothing else.
type: regex
target: last_message
pattern: '_new_ref|max\(self\._bookings|(?:breaks?|against|violat\w+|contradicts?)\s+ADR-0001|references?\b[^.\n]{0,80}?\b(?:re-?(?:us|issu)|issued\s+again)|\bre-?(?:us|issu)\w+\b[^.\n]{0,80}?\breferences?\b'
flags: i
---
