---
type: llm
focus: { source: file, path: output.md }
---
Find the doc comment on `Firing::take_reading`. The original read:

> Takes the next reading from the thermocouple and folds it into the fault count. Three in a row abort the firing (0003); a good reading resets it, and a fault short of the third reports the last good temperature instead.

The first sentence looks like a restatement of the name, but it is the only place "the fault count" is introduced: "Three in a row" means three faults in a row, and "resets it" means resets the fault count. If the first sentence is cut and nothing is repaired, "Three in a row" has no noun and "it" reads as "the firing".

PASS if the comment survives with the abort rule, the reset by a good reading, and the last-good-temperature behaviour, and every one of those still says what it refers to: either the original first sentence (or another sentence naming the fault count) is still there, or the remaining text has been repaired so that it names faults and the count explicitly (for example "Three consecutive faults abort the firing (0003); a good reading resets the count").
FAIL if what survives has "Three in a row" with nothing saying three of what, or a pronoun such as "it" whose nearest reading is the firing rather than the count, or if the reset rule or the last-good-temperature behaviour has been dropped.
