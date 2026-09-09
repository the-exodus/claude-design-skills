---
name: design-philosophy
description: The design principles that govern how software here gets structured — complexity as the thing to minimize, deep modules behind small interfaces, information hiding, no pass-through layers, pushing complexity down rather than out, considering alternatives before committing, and favoring long-term simplicity over short-term speed. Load this when designing new functionality, deciding how to decompose or structure a change, weighing two approaches against each other, reviewing structure rather than syntax, or implementing from a spec or prompt where the structural decisions are still open. The design-interview skill invokes this at tree seeding. Code-level style — formatting, naming conventions, comment mechanics — is not here.
---

# Design Philosophy

These principles apply in two situations: when a design is being worked out, and when an agent is implementing from a spec or a prompt and still has structural decisions to make. They're the same principles both times; what differs is whether they generate questions or constrain code.

They are not a review checklist to run at the end. A principle applied after the structure exists can only produce regret. Applied while the structure is being chosen, it produces a better structure.

## The principles

### Complexity is the enemy

Every decision gets judged by one question: does this make the system easier or harder to reason about? Prefer the option that reduces total complexity, even if it takes more work now.

This is the root principle; the rest are specific ways of applying it. When two of the others conflict, this is the tiebreaker.

**At design time:** at every fork, ask which option is easier to reason about in six months, and make the answer part of the closure rationale. An option chosen because it was faster to describe is not an option chosen.

**At implementation time:** when the spec leaves latitude, spend it on comprehensibility rather than cleverness.

### Interfaces should be simpler than implementations

Modules should do a lot behind a small, clean interface. If a module's interface is nearly as complicated as what it does internally, it isn't pulling its weight — either deepen it or eliminate it.

**At design time:** for every module or component the design proposes, this is a branch, not a review note. What must a caller know to use it? How much does it do? If those two are close, the module is a cost with no benefit.

**At implementation time:** the signal is a caller that has to understand the implementation to call it correctly. Ordering requirements, initialization dances, and flags that change what a function fundamentally does all mean the interface leaks.

### Hide decisions, not just code

Decomposition should be based on what knowledge needs to stay encapsulated, not just on splitting by function. If changing one thing requires touching many modules, information is leaking across boundaries.

**At design time:** for each proposed module, ask what knowledge it owns exclusively. Then take a likely future change and ask how many modules it touches. A decomposition that looks tidy but spreads one decision across four files is worse than an untidy one that contains it.

**At implementation time:** splitting a file because it got long is not decomposition. Ask what each piece would own.

### No pass-through layers

Each layer of abstraction should do something meaningfully different from the one above it. Layers that just forward calls or data unchanged are a smell.

**At design time:** for every layer in the proposal, state what it does that its neighbor doesn't. If the answer is "it calls the next one down," delete it.

**At implementation time:** a method that exists only to call one other method, a type that exists only to be converted to another type, and a config that only reformats another config are all the same defect.

### Push complexity down, not out

When something has to be complicated, better it lives inside a module — written once — than in its callers, where it is paid for many times.

**At design time:** count callers. Complexity in a module is paid once; the same complexity pushed to callers is paid per call site, forever, by people who have less context than the module's author had.

**At implementation time:** this is the argument against making the caller handle a case the callee could have handled. A function that returns something the caller must always post-process has pushed its work outward.

### Consider alternatives before committing

Sketch at least two approaches to any non-trivial component before building, even roughly. The first design is rarely the best one.

**At design time:** this is strong enough to be a closure requirement, not a suggestion. A branch that closed *decided* with only one approach ever named didn't get decided; it got defaulted. Before closing, name the alternative you rejected and why — and if you cannot name one, say that out loud, because it usually means the space wasn't looked at.

**At implementation time:** applies to anything non-trivial the spec left open. Two sketches, briefly, before committing to one.

### Optimize for long-term simplicity over short-term speed

Favor the slightly slower, cleaner path over quick hacks that add hidden debt, unless there's a real reason not to.

"Unless there's a real reason not to" is load-bearing: deadlines are real, and a deliberate, recorded shortcut is a legitimate engineering decision. An undiscussed one is not.

**At design time:** when a shortcut wins, record it as a decision with its cost stated, not as a silent default. The closure rationale is where the debt gets written down.

**At implementation time:** if you take the fast path, say so and say what it costs.

### Be consistent; generalize modestly

Reuse naming and patterns across the codebase. A module built for the general case is often simpler than one narrowly special-cased for today's use.

Both halves have a failure mode, and the second one's is worse. Modest generalization means the general case when it's *simpler* — not speculative extension points for requirements nobody has. A special case that pretends to be a framework is more complex than either honest option.

**At design time:** ask whether this already exists under another name. Then ask whether the general version would be simpler than the special case — if it wouldn't, build the special case.

**At implementation time:** match the surrounding code's idiom even where you'd personally do it differently. Consistency is a property of the codebase, not of any one change.

## Boundary: what isn't here

**Comments justify, code describes.** Code says what it does; comments should say why, what isn't obvious, and what invariants matter. If a comment just restates the code, delete it.

This one is in the set philosophically but is really coding style — it governs how code reads, not what gets decided. It's recorded here so it isn't lost, and it should move to the coding-style skill when that exists.

The line: **a principle that changes what gets decided is design; a principle that changes how code reads is style.** Formatting, naming conventions, comment mechanics, import ordering, and test structure are all style. Everything above is design.
