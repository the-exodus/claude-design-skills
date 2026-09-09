# Functional Specification

## What it's for

What the system does, stated precisely enough to implement without asking follow-up questions. This is where "we decided X" becomes "when the user does Y, here is exactly what happens."

Always required. It is the artifact the others hang off.

## Scope note

Behavior, not structure and not mechanism. *What* happens, under what conditions, in what order, with what result. How it's built is implementation and was gated out of the interview on purpose — don't smuggle it back in here. If a paragraph would only matter to someone reading the code, it doesn't belong.

## Must contain

**Scope and non-goals**, both explicit. The non-goals come from branches closed *out-of-scope* and *deferred-later*, with their stated reasons. This section is not padding: it is the record of what was deliberately not built, and it is the first thing a future reader needs in order to not re-litigate a settled question.

**The behavior itself**, organized by what the system does rather than by what module does it. For each behavior:

- The triggering condition — who or what initiates it, and when.
- The preconditions that must hold, and what happens when they don't.
- The rules applied, stated so that two readers compute the same result. Where multiple rules can apply to one case, the precedence order, explicitly. "Whichever is more restrictive" is a valid rule and must be named as one.
- The observable result — what changed, what the initiator sees, what anyone else sees.
- The side effects, and when they fire relative to the primary result: at request, after commit, on a delay. Whether each is durable or best-effort.

**State and lifecycle**, wherever an entity moves through states. Every state, every legal transition, what causes each, and which states are terminal. A state with no documented exit is a bug in the design, not a gap in the writing — report it.

  When the lifecycle is complex — many states, guarded transitions, transitions that depend on more than the current state — render this section as a table or a diagram rather than prose. That is a presentation choice inside this artifact, not a reason to split it into a separate one.

**Rules, in one place.** Business rules scattered through behavior descriptions get implemented three different ways. Where a rule governs more than one behavior, state it once, name it, and reference it.

## Completeness test

**A reader can determine the system's response to any input the spec claims to cover, without inference and without asking you.**

Sharper version, and the one worth actually running: **the acceptance criteria artifact can be written from this document alone.** If writing a test case requires going back to the tree or making something up, this spec is incomplete at that point. That is not a reason to soften the test case — it is a gap to report.

## Common failures

- **Describing the happy path as though it were the behavior.** The failure and edge behavior lives in its own artifact, but the spec must be complete for the cases it does cover, and must point at the edge-case artifact rather than pretending the edges don't exist.
- **Stating rules with unstated precedence.** Two rules that can both apply and no ordering is one of the highest-yield defects to catch here.
- **Restating decisions instead of specifying behavior.** "We decided to use optimistic updates" is a tree entry. "When the request fails, the local change reverts and the prior value is restored" is a spec.
- **Leaving a state with no exit.** Anything that can be entered and not left is a stuck state; the interview's expiry pattern should have caught it, and if it didn't, that's a branch to reopen.
- **Silently resolving a deferred branch.** If the tree deferred it, the spec says it's deferred. Writing behavior for it makes the deferral invisible.
