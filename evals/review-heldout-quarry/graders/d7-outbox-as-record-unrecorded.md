---
# D7: who was notified is inferred from the outbox files, an unrecorded decision. A correct report may name the function or describe the choice ("the outbox says who was told").
type: regex
target: last_message
pattern: 'notified_receptors|who was (?:told|notified)|outbox (?:says|is the record|as the record)|record(?:ing)? (?:the )?notified'
flags: i
---
