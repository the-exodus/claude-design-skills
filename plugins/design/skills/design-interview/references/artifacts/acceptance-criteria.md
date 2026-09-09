# Acceptance Criteria

## What it's for

The sharpest available test of whether the design is complete and whether an implementation is faithful to it. Always required, and written last, because it is the proof of everything above it.

The claim it makes concrete: **if test cases can be written from the design alone, the design is done. If they can't, there's a gap.** That makes this artifact a measuring instrument, not just a deliverable — its failures are more informative than its successes.

## Must contain

**A case per behavior in the functional spec**, in given / when / then form or any form that names preconditions, action, and expected observable result. Vague expectations defeat the purpose: "the request succeeds" is not a criterion; "the record exists with status `accepted` and the caller receives its identifier" is.

**A case per entry in the edge-case artifact.** Boundary values, malformed input, concurrency, partial failure, stuck states. These are the criteria that actually catch regressions; the happy-path cases mostly catch typos.

**Observable results only.** A criterion asserting on internal structure — a helper was called, a field is arranged a certain way — tests the implementation rather than the design, and will break on refactors that changed nothing anyone can see. Assert on what a caller, a user, or an operator can observe.

**Explicit non-criteria**, where useful: behavior deliberately unspecified, so that an implementer knows they have latitude rather than guessing at an unstated requirement. Branches that closed *deferred-implementation* are exactly this, and naming them here is what makes that terminal state useful downstream.

## Completeness test

Applied to itself, and to everything upstream:

- **Every decided branch is represented by at least one case.** A decision with no criterion is a decision nobody will check.
- **Every case traces to something decided.** A criterion you couldn't source is a requirement invented at write-up time; mark it as inference or drop it.
- **No case requires reading the tree to understand.** These are for someone implementing from the documents, who does not have the conversation.

## Common failures

- **Softening a criterion because the design didn't settle it.** This is the failure that matters most. Vagueness here is where an unclosed branch gets laundered into a document that looks finished. Report the gap instead; that is the entire value of writing this artifact.
- **Only happy paths.** The edge-case criteria are the ones worth having.
- **Asserting on internals.** Tests the code, not the design.
- **One giant case per feature.** A case that checks eleven things tells you nothing useful when it fails.
- **Criteria that restate the spec sentence.** If it isn't checkable, it isn't a criterion.
