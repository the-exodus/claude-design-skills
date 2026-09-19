# Output Artifacts

Read this at Phase 9, before writing anything.

## Where artifacts go

**Nothing here has a hardcoded path.** The destination comes from the project, and Phase 2 already worked it out: whatever its scans found — ADRs, a lexicon, an assumptions record — establishes where this project keeps design documentation. Write the durable artifacts alongside it; write the feature's brief where the project's conventions say the build reads it (see *Which artifacts this design needs*).

If the scans found nothing and no documentation directory is obvious, ask. Once, in one line, **with a concrete suggestion** — one that fits what the repo actually looks like, its ecosystem's convention or a `docs/` that already exists, rather than a preference of your own. Use the answer for everything in this capture.

Ask at most once per project. After this, the files exist and Phase 2's scan finds them, so the destination is derived rather than asked.

Keep the artifacts together, and keep their names recognizable, because the next interview's scan has to find them.

## Provenance

Artifacts need detail the design tree does not always carry. The tree records decisions; a functional spec records behavior, a data model records constraints, acceptance criteria record cases. Some of that was decided in the interview. Some of it will be you filling gaps.

Both are acceptable. Only one is acceptable *silently*.

- A statement tracing to a branch closed **decided** is written plainly.
- A statement you inferred is **marked as inference, inline, with what it was inferred from.** Not collected in a footnote at the end where it reads as afterthought.
- A statement that would resolve a branch closed **deferred**, **blocked**, or **stable-open** is not written at all. Those are open on purpose, and quietly closing one in prose destroys the reason they were left open.

Never let the two look alike. A document where agreed decisions and plausible invention are typographically identical gets implemented as though all of it was agreed.

## Capture is a completeness check

Anything an artifact needs that the tree doesn't have is a gap in the interview, not a gap in your writing. Treat it that way.

When a section can't be written from decided branches:

1. Name the branches that are missing, or that closed too loosely to write from.
2. Offer to reopen them. This is a normal continuation of Phase 5 and the four locks still apply.
3. Write the section on marked inference only if the user declines.

Reaching the end of capture with no gaps to report is real evidence the interview was thorough. Reaching it having invented a third of the content and said nothing is the failure this phase exists to prevent. **Report the gap count even when it is zero.**

## Vocabulary

Every artifact uses the lexicon, and only the lexicon, for anything the lexicon names. Artifacts diverging on terminology is the specific failure the lexicon exists to prevent, and it shows up here first — the data model calling something a `member` while the contract calls it a `user` is how two correct-looking documents produce two different systems.

A term the artifacts need that isn't in the lexicon is a gap like any other. Surface it; don't quietly coin one.

**Write the lexicon back.** Whenever capture runs, the consolidated lexicon is written back to where it was ingested from, or to the destination established above if there wasn't one. This is unconditional and it is not optional: the artifacts are written in this vocabulary, so a reader without the lexicon has documents whose terms mean whatever they assume. It is also what the next interview ingests. Show which entries are new and which changed before writing. An inherited entry changes only where this design changed what the word means.

## Assumptions and tracker candidates

**Write the assumptions record back**, to where it was ingested from, or to the destination established above. Unconditional, like the lexicon, and for the same reason: it is not a deliverable, it is what the next interview reads, and what a review of the build checks its platform assumptions against.

It holds the assumptions still standing, each with a stable id, the assumption in one line, the subject area, and **how you would know it stopped holding** — an assumption recorded without that is decoration; with it, a later interview can actually check — plus the facts the project has measured that would cost time to rediscover. Remove an assumption the interview invalidated rather than annotating it; if the resolution was a real fork it became an ADR, and that is where the history belongs.

**Branches closed *deferred-later*, *blocked*, or *stable-open* are not written to a file.** They are the next design questions, and a file of them turns into a backlog the tracker already is. Emit them as tracker candidates: one line each with the question, why it is open, and **what would resolve it**, for the user to file. The next interview asks which tracker items touch its work.

## Which artifacts this design needs

**Two outlive the feature: the decision records and the lexicon** (and the assumptions record, above). They are kept in the tree and kept true. Everything else in the tables below is **the feature's brief**: it tells the build and its reviewers what was decided, in the detail the tree does not carry, and it is spent when the feature ships — the code is its own domain model and interface contract, the tests carry the criteria, the project's references carry the behaviour. Write the brief where the project's conventions say the build reads it: on the tracker issue when the project works from one, else in the documentation directory marked as a brief. Do not carry a brief into the next interview as if it described the system; scan the code and the durable three instead.

Four are unconditional:

| Artifact | Template |
|---|---|
| Decision records (ADRs) | the `design:adr` skill — see below |
| Functional specification | `artifacts/functional-spec.md` |
| Edge cases and error handling | `artifacts/edge-cases.md` |
| Acceptance criteria | `artifacts/acceptance-criteria.md` |

The rest are selected by the same conditions check that seeded the tree (`conditions-and-patterns.md`). If the condition held at seeding, the artifact is required now:

| Artifact | Required when | Template |
|---|---|---|
| Interface / contract definitions | *Callers you can't change in lockstep*, or any boundary between components that ship or evolve separately | `artifacts/interface-contract.md` |
| Domain model | *The same concept has more than one shape*, *state outlives a single version*, *holds data that belongs to someone else* | `artifacts/domain-model.md` |
| Non-functional requirements | *It runs inside a constrained envelope*, *someone operates it in production* | not yet templated |

There is deliberately no state-machine artifact. State and lifecycle content is unconditional and lives in the functional spec, which already requires every state, every transition, and every terminal state. A separate artifact would reformat content another artifact owns — a pass-through layer. Where a lifecycle is complex enough to need a diagram, the spec renders it as one.

### Decision records

**Every ADR-worthy decision gets an ADR, always.** Not conditional, not on request, not deferred to the user's judgment at write-up time. Invoke the `design:adr` skill and let it write them — it owns format, house rules, numbering, indexing, and supersession, and none of that is reimplemented here.

A branch that closed *decided* is ADR-worthy when it meets all three:

- **A real fork existed.** The closure recorded it as a fork, with the alternatives and why each was rejected. Read that line; don't reconstruct it from the rationale. A closure recorded as *no fork* is not an ADR no matter how consequential it feels — nothing was chosen.
- **The consequences outlive the change.** It constrains later work, or reversing it later would be expensive.
- **A future reader would ask why.** The choice is not self-evident from the code that results.

Not ADR-worthy: decisions with only one option ever available, choices forced by an existing constraint, anything the design-vs-implementation gate would have deferred, and anything an indexed ADR already covers.

Two cases need care:

- **A decision that contradicts an ADR indexed in Phase 2** is a supersession, not a new record. Say so and hand the `design:adr` skill both — it owns what happens next. ADRs are superseded, never edited.
- **A branch that closed *stable-open* or *blocked*** is not a decision and gets no ADR. Leave it in the tree where its openness is visible.

Give the `design:adr` skill, per decision: the question, the options considered **and why each was rejected**, the chosen path, the rationale from the closure, and any ADR it supersedes. The rejection reasons are not optional padding — they are what makes the record load-bearing later, when someone is weighing the same option again and needs to know it was already ruled out and on what grounds. Then let it work.

For an artifact marked *not yet templated*, write it from the general rules on this page: provenance, lexicon discipline, and a stated completeness test of your own before you start.

## Common shape

Every artifact opens with the same three lines, because a reader needs them before the content:

- **Sourced from:** the design tree of [date/topic], N branches decided.
- **Gaps:** what could not be written from decided branches, or "none".
- **Inference:** how much of this document is marked inference, in one sentence.

Then the artifact's own content. No preamble, no restating the pitch, no summary of the interview. The reader wants the design, not its history.
