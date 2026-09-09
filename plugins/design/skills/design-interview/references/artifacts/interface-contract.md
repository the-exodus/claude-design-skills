# Interface / Contract Definitions

## What it's for

The explicit agreement between two things that talk to each other and don't ship together. Prose is not a contract: if the shape can only be inferred by reading a paragraph carefully, two implementers will infer differently, and the failure shows up at integration time when both are already built.

Required when *callers you can't change in lockstep* held at seeding, or wherever a boundary exists between components that evolve on separate schedules.

## Scope note

This is the contract, not the implementation and not the behavior behind it. What a call *does* belongs in the functional spec; what it *accepts, returns, and guarantees* belongs here. If you find yourself explaining business rules, you've crossed over — put them in the spec and reference them.

## Must contain

**The surface itself**, in whatever notation fits — signatures, schema, IDL, DDL, message shapes. Notation over prose wherever a notation exists. A signature is unambiguous; a sentence describing a signature is not.

For every element of the surface:

- **Required vs. optional**, with the default for anything optional. "Optional" without a default is not a contract.
- **Unknown fields:** rejected, ignored, or preserved and passed through. Pick one and say it — this is the single most common thing to leave unstated and the most expensive to change later.
- **Types and permitted values**, including which are open sets that may grow and which are closed sets a caller may exhaustively switch on.

**The failure surface**, treated with the same weight as the success surface:

- Every error a caller can receive, by identifier, not by prose description.
- Which are retryable and which are terminal. A caller cannot write correct retry logic from an error list that doesn't say.
- Whether errors are an open set. If new ones can appear, say so, or every caller's exhaustive match breaks on your next release.
- Distinctions that carry meaning at the boundary — not-found versus not-permitted, invalid versus conflicting — and what each discloses.

**The guarantees**, which is the part most often missing entirely:

- Idempotency: which operations are safe to repeat, at what granularity, and keyed on what.
- Ordering: what is guaranteed to arrive or apply in order, over what scope.
- Atomicity: what succeeds or fails together, and what can partially apply.
- Timing: timeouts, deadlines, and whether they're the caller's or the callee's to enforce.

**The evolution rules:**

- How a caller discovers which version it's talking to.
- What changes are permitted without a version bump, stated as a rule rather than case by case.
- The deprecation and removal path for anything here.
- Whether old and new can coexist, and for how long.

**Authorization**, if the boundary is a trust boundary: what the caller must present, what is decided on which side, and what a caller is allowed to conclude from a refusal.

## Completeness test

**Two people could implement opposite sides of this contract, in different languages, without talking to each other, and the halves would work.**

Concretely, all of these must be answerable from the document alone:

- Given a malformed request, what exactly comes back?
- Given a call that times out, is it safe to retry?
- Given an unrecognized field or value, does it fail or pass through?
- Given a new version of the other side, what still holds?

Any "it depends" is an open branch. Report it as a gap.

## Common failures

- **Documenting the happy path in detail and errors in a sentence.** Callers spend most of their code on the failure surface; it deserves most of the contract.
- **Prose where notation exists.** If a schema language covers it, use the schema language.
- **Silently deciding the unknown-field rule.** It is a real decision with real consequences, and if the tree didn't settle it, that's a gap, not a default you get to pick.
- **Omitting guarantees because they felt obvious.** Idempotency and ordering are obvious to whoever wrote the implementation and invisible to everyone else.
- **Describing internals.** If a caller doesn't need it to make a correct call, it isn't in the contract. The interface should be simpler than what it hides.
