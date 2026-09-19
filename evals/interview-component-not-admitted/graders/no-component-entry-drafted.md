---
# No lexicon entry is drafted for the component. An entry is a bold headword followed by a dash.
type: regex
target: last_message
pattern: '\*\*`?(?:StationHealth|health\.py|health block|station health)`?\*\*\s*[—–-]'
flags: i
match: not_contains
---
