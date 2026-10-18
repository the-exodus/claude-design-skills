---
name: code-style
description: >
  Load first, before the first Edit or Write, whenever a request will have you
  choose or change a name, or write or change a comment or the code it sits in
  — a rename, a pass over comments or docstrings, a feature, a bug fix, a
  refactor — however mechanical it looks. A rename is nothing but a naming
  decision, and how a name or a comment reads is decided as it is written; these
  principles govern both here. Carries the house rules for names (name it what it is, call it
  what it does; domain words from the lexicon) and for comments (say what the
  code cannot: delete what the name, signature and code in view already say,
  keep what depends on context that lives elsewhere, and shrink a comment that
  mixes both, clause by clause). Trigger on implement, add, fix, refactor,
  rename, comment, document, tidy, clean up. NOT for a typo in prose or a
  formatting change that alters no name and no comment.
---

# Code style

**Name it what it is. Call it what it does.**

**Comments express what the code can't, and only that.** If the code expresses it, do not write the comment: it is superfluous, and it goes stale.

## Names

- **Domain words come from the project's lexicon** (a lexicon or glossary, wherever the project keeps it). The code takes its names from the lexicon, never the other way round. Do not rename a domain term to a word you like better, and do not coin a synonym for one; a domain word the lexicon lacks is a question for `design:lexicon`, not a name to invent.
- **Every other name is the code's own**, and says what the thing is or what it does for its caller: `parse_invoice`, `RetryBudget`. Not its type (`user_dict`), not how it is built (`poll_until_ready`), and not a word that fits anything (`Manager`, `Helper`, `Util`, `Data`, `handle`, `process`).
- A name that says it all needs no comment. Do not explain a name you just chose.

## Comments: locality is the test

Judge a comment **clause by clause**, not whole. For each clause, ask: could a reader get this from the name, the signature and the code in view?

| Where the context the clause carries lives | Then |
|---|---|
| In view: the name, the signature, the body of a short member, the lines beside it | **Delete** the clause. |
| Elsewhere: a platform or library behaviour, a decision recorded somewhere else, an invariant another type enforces, what a caller must do or can rely on, where the member sits in a flow (which callers reach it, what has already happened by then), a reason someone gave | **Keep** the clause. |
| A comment with clauses of both kinds | **Shrink** it: cut the clauses in view, keep the rest. |

- **Cut at the clause, not the sentence.** A summary often opens by saying again what the name says, then goes on to a contract ("X happened and Y has run: the caller must…"). The clause that repeats the name goes even when "and" ties it to one that stays, and even when it says the name in other words: a synonym, or the domain's word for what the name calls by its mechanism.
- **A re-listing or a quotation goes stale.** A clause that lists values the code defines elsewhere (the other codes beside this one, an enum's members) or quotes another member's documentation is a copy, and it is the half that rots. Cut it and keep the reason it was there for. A member's own contract is not a copy: it stays on the member, where a caller reads it, even when its class says the same.
- **In a test, the test's name and its body are the code in view.** A comment that says what the name says, or what the asserts below it check, goes. One that says what the body cannot show stays: a race between threads, what the harness is standing in for, why the rule under test exists.
- **Go through every comment, not a sample.** In a file whose comments are mostly right, the leftovers are summaries whose first clause says the name again; read each one's opening against its member's name.

- **The common case is keep.** A codebase built from deep modules hides context on purpose, and an interface comment that carries what the hidden implementation does not show is the module working as designed, not a sign the code is unclear.
- **Keeping is not encouraging.** Write a comment only when it carries something from elsewhere. A summary on every member, or a comment added because a principle seems to want one, is the same failure as a missing one.
- **While writing code**, the test turns round: if writing a line made you look something up outside the code in view (a protocol, a platform quirk, another module's invariant, a reason the user gave you, a decision too small for a record), say it where the line is, in a comment or in a name. If you only chose a name, say nothing.

### A shrink is more dangerous than a delete

A delete is visible. A cut clause quietly breaks the sentence that depended on it, and no test sees it. After every shrink, re-read what remains as someone who never saw the original:

- **A reference cut loose.** A pronoun or "the X" whose referent was in the clause you cut. Repair it with the noun, or do not cut.
- **A qualifier cut.** Words that look like they restate the name may be limiting its scope ("every write *the cache accepts*"). Without them the comment claims more than the code does. Keep them.
- **A why turned into a what.** "Used to copy alerts to the pager out of hours" is a purpose; "Copies alerts to the pager" claims a behaviour the code may not have.
- **Nothing added.** A tidy cuts and repairs. It adds no fact, condition, number or narrowing the original did not state.

Before deleting a whole comment, ask what in it is recorded nowhere else. A comment that looks redundant is sometimes the only record of why ("five attempts, *as the supplier's contract allows*").

### Citations

- **A citation never stands in for a claim.** A comment that only points at a record ("See ADR-0012.") is deleted: the record can be found from the code it governs, and a pointer says nothing when the record changes. Where a citation is allowed, it sits beside the comment's own words.
- **Cite by number, never by title.** A title changes; a number does not.
- **The project's own convention wins.** Where it excludes citations, often in tests, introduce none, and when tidying drop the citation and keep the claim. A test-file summary that restates what a decision record says is deleted, not replaced with a pointer, unless the project says otherwise there.
