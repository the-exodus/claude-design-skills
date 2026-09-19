---
type: llm
focus: last_message
---

This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "layout" entry, "When a workspace holds a single window, every layout gives it the whole work area."

The written lexicon is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (a lone window gets the whole work area), among the homeless content or as having no other home.
FAIL if the report gives the doc comment in src/Tessera/Workspaces/Workspace.cs at or around lines 70-71 as a place where that statement lives. This fails even when the report names the true home beside it: that comment mentions the single-window case without saying what happens, so it is not a home.
PASS in every other case: the report names src/Tessera/Layouts/ILayout.cs (a doc comment) as its home, or says the statement stays in the entry, or does not say where it went. Citing other lines of Workspace.cs, or citing it for other content, does not fail.
