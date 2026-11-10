---
# D1: _new_ref reuses a settled hold's reference, against ADR-0001. A correct report may name the function, quote its max(...) or say in words that references are reused or reissued.
type: regex
target: last_message
pattern: '_new_ref|max\(self\._bookings|references?\b[^.\n]{0,80}?\bre-?(?:us|issu)|\bre-?(?:us|issu)\w+\b[^.\n]{0,80}?\breferences?\b'
flags: i
---
