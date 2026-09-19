---
type: llm
focus: { source: file, path: output.md }
---

This is one reply from an assistant that has just written an updated lexicon file for a project after a design interview. Five entries were inherited (cycle, reading, stale, station, station list) and two were added by the interview (miss, silent). Judge one thing only.

PASS if the reply tells the user which entries are new (miss and silent) and says that no inherited entry changed, or lists exactly which did.
FAIL if the reply does not distinguish new entries from changed ones, or claims an inherited entry changed when the interview left all five as they were.
