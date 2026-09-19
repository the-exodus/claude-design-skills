---
type: llm
focus: { source: file, path: output.md }
---

This is one reply from an assistant running a software design interview. The project has a lexicon: the domain words its documents use, each with a fixed meaning. At the end of a branch of the interview the assistant says which words, if any, it admits to the lexicon. Judge one thing only.

The lexicon the project already had defines *stale* like this: "**stale** — Said of a *reading* older than two *cycles*. A stale reading is still shown; it is not the same as having no reading." The user's message closed a branch by deciding how a stale reading is drawn (its age is now shown beside the greyed number) and said that *stale* keeps its meaning.

PASS if the reply leaves the *stale* entry as it is: it says the entry is unchanged or untouched, or does not propose any change to it.
FAIL if the reply proposes to amend, extend or rewrite the *stale* entry, for example by adding that a stale reading is shown with its age, or by redefining it in terms of silence.
A decision about how stale readings are displayed, recorded as a decision of the design, does not fail.
