---
type: llm
focus: { source: file, path: output.md }
---

This is a report on consolidating a project glossary. Judge one thing only: what it says about the sentence from the old "dry period" entry, "A cow whose dry period will be shorter than 40 days is marked as short on the calving list."

The written glossary is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (a dry period under 40 days is marked short), among the homeless content or as having no other home.
The decoy is one doc comment: the comment on the Calving list in internal/lists/builder.go, lines 49-50, which reads "...soonest first, and marks the cows heading for a short dry period." It mentions a short dry period without giving the 40-day threshold, so it is not a home for the sentence.

FAIL if the report gives that comment, builder.go lines 49-50, as a place where the statement lives. This fails even when the report names the true home beside it.
PASS in every other case: the report names internal/lactation/lactation.go (a doc comment) as its home, or says the statement stays in the entry, or does not say where it went. A citation of builder.go from line 54 on, the code that applies the mark, is not the decoy and does not fail, whether alone or beside the true home: code that implements the behaviour is fair evidence.
