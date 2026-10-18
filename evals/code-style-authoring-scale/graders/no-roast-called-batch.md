---
# Domain words come from the lexicon. A roast is never a batch here, so no new function, class or variable names a roast "batch"; `batch_lot`, the lexicon's own sense, is the one allowed use.
type: regex
target: { source: file, path: roastlog/log.py }
pattern: '\b(?:def|class)\s+\w*[Bb]atch(?!_lot)|\b(?!batch_lot\b)\w*batch\w*\s*=\s*Roast\('
match: not_contains
---
