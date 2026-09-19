---
type: llm
focus: { source: file, path: output.md }
---

This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "layout" entry, "When a workspace holds a single window, every layout gives it the whole work area."

The written lexicon is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (a lone window gets the whole work area), among the homeless content or as having no other home.
The decoy is one doc comment: src/Tessera/Workspaces/Workspace.cs, lines 70-71, which reads "Callers that draw borders care about the single-window case, which the layouts treat specially." It mentions the single-window case without saying what happens, so it is not a home for the sentence.

FAIL if the report gives that comment as a place where the statement lives: a citation of Workspace.cs whose lines include 70 or 71, offered as where the single-window behaviour is stated. This fails even when the report names the true home beside it.
PASS in every other case: the report names src/Tessera/Layouts/ILayout.cs (a doc comment) as its home, or says the statement stays in the entry, or does not say where it went. Citing other lines of Workspace.cs, or citing it for other content, does not fail.
