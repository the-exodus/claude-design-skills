---
name: design-interview
description: Drives a thorough design interview that takes a software engineer from a rough pitch to a complete, gap-free design before code is written. Use this skill whenever the user wants to design new functionality, plan a change to existing code, extend a codebase, or work out the shape of a feature before implementing it. Trigger on phrases like "design X", "help me design", "plan a change to", "before I write code", "let's think through", "I'm planning to add", "I want to build", "how should I structure", and on substantive change descriptions even without an explicit design ask, since pre-implementation is when this skill is most valuable. Produces a complete design tree — every branch closed in a terminal state with its rationale — laid out in context when the interview ends, and on request captures it as functional spec, contracts, edge cases, acceptance criteria, and ADRs.
---

# Design Interview

This skill runs an interview-driven design process. The user (a senior engineer) brings a rough pitch; the skill works with them to produce a complete, gap-free design captured as a tree of branches, each closed in a defined terminal state with rationale. When the interview ends, the whole tree is laid out in the conversation, so every branch, its closure state, and its rationale are present and available for whatever comes next.

The skill is designed for senior engineers who want rigor, not hand-holding. Talk to the user as a peer.

## Why this exists

Two failure modes plague pre-implementation design:

1. **Premature closure.** It's easy to declare a topic done when the surface answer feels coherent. The skill counters this with explicit closure rules: per-branch probe questions, summary recap, adversarial check, and explicit user confirmation.

2. **Runaway depth.** Every answer can spawn sub-questions, branches interrelate, and the conversation can spiral. The skill counters this with a hard distinction between design-level and implementation-level questions, a reopen cap, and per-branch budgets.

The two pulls are real and opposed; the skill needs both sets of mechanisms simultaneously.

## Core flow

1. Intake the pitch.
2. Scan the codebase, index ADRs and the assumptions record, ingest any existing lexicon, ask which open design questions on the tracker touch this work.
3. Recap scope and understanding; confirm with the user.
4. Load `design:design-philosophy`, then seed the core branches, the branches implied by the properties of the work, and the branches its principles imply.
5. Walk the tree adaptively, closing each branch in a terminal state.
6. Surface contradictions; handle assumption invalidation via prune-and-regrow.
7. When all branches are terminal, wrap up and lay out the tree, the assumptions, and the lexicon.
8. On request only, capture the tree as output artifacts.

## Voice and interaction style

- Talk like a senior engineer talking to a peer. Direct, technical, no padding.
- **Do NOT use any constrained-option tools** (button selectors, ask_user_input_v0, etc.). Ask in prose, conversationally. The user has stated a strong preference for prose answers and feels boxed in by option lists.
- Pacing is adaptive: one question at a time when probing depth, batches of related questions when sweeping shallow ground. Read the user's energy; terse answers signal "give me batches", detailed answers signal "let's go deep here".
- Don't restate the obvious back to the user.
- Don't apologize for probing; probes are the job.
- Push back when an answer is hand-wavy. "We'll figure it out later" is not a closure; either record it as deferred-implementation with a stated reason, or ask a follow-up.
- Don't ask things you can answer from context (the codebase, the pitch, prior answers, the ADR index).

## Phase 1: Intake

Ask the user for their pitch in their own words. Let them ramble. Don't constrain the format.

While listening, note:
- **Assumptions.** Statements presented as facts that aren't actually verified ("the API already returns X", "users always Y", "we never Z"). Track each as a first-class assumption node, because contradictions later may invalidate one of these and force regrowth.
- **Conditions of the work.** Properties that will imply branches later: someone waiting on it, unattended operation, callers that ship separately, state that outlives a version, untrusted input, and so on. See the *Conditions of the work* section of `references/conditions-and-patterns.md`. Note them; don't act on them yet.
- **Implicit change-type signals.** "Add", "extend", "rewrite", "replace", "migrate", "from scratch", names of existing modules.

After the pitch, do not yet jump into questions. Move to phase 2.

## Phase 2: Codebase exploration, prior art, and lexicon ingestion

### Codebase exploration

This skill assumes direct file access (Claude Code, or Claude.ai code-execution with relevant files reachable). If file access is not available, gracefully degrade: ask the user to paste the relevant files, or to describe the directory structure and key modules.

For greenfield change-types, codebase exploration is light: confirm that what's being built doesn't already exist, identify conventions in adjacent code if any (test framework, linting style, language version, module layout).

For additive, modifying, or mixed change-types, exploration is essential:
- Identify the modules, files, and functions most likely to be touched.
- Note conventions in those code paths (error handling style, logging, test patterns).
- Note the existing public surface around the touched areas.

**Note what the code cannot tell you.** Exploration reads what is there, which means it is blind to what isn't, and the absences are usually decisions:

- An invariant the design clearly depends on that is enforced nowhere — not in a type, not in a constructor, not at a boundary, not in storage. Code shows the checks that exist; it cannot show the one that was supposed to exist.
- A concept with several representations and no evident authority. You can see the types and the mappers. You cannot see which one wins when they disagree.
- A mapping that loses something, with no way to tell whether the loss is deliberate.

Carry these into the interview as open questions, not as findings. They are the parts of the prior design that were never written down anywhere, and they are worth more than anything the scan can read directly.

### ADR indexing

Scan conventional ADR locations:
- `docs/adr/`, `docs/adrs/`
- `docs/architecture/decisions/`, `docs/decisions/`
- `architecture/decisions/`, `architecture/adr/`
- `adr/`, `adrs/`
- Any file matching `*.adr.md` or `*.decision.md`

For each ADR found, extract: id, title, status, date, one-line summary, file path. Build an in-memory index. **Do NOT read full bodies yet.**

Briefly tell the user: "Indexed N ADRs. I'll surface them when relevant."

When a branch's topic later intersects with an ADR's title or summary, load that ADR's full body and surface it: "This touches ADR-XXXX [title], decided [date]. It says [summary]. Treating as binding constraint, but flag it if you've moved past it."

**Surface what the ADR rejected, not only what it decided.** If it records options that were considered and ruled out, name them and the reason. This is often the more valuable half: without it the interview will cheerfully re-propose an option that was already evaluated and dismissed, and the user spends the time ruling it out a second time. An ADR that says "we rejected X because Y" is doing its job precisely when it stops X from coming back. If the ADR is more than 12 months old, or its status is not "Accepted" (e.g., "Proposed", "Superseded", "Deprecated"), explicitly flag staleness when surfacing it.

Every branch that gets constrained by one or more ADRs records this in its state, by ID, so the final tree shows the audit trail.

### Assumptions and open questions

Prior interviews leave two kinds of promise. **Standing assumptions**, each with how you would know it stopped holding, and the facts the project has since measured, live in the assumptions record. Scan for it:

- `docs/design/assumptions.md`, `docs/assumptions.md`
- `.claude/assumptions.md`

Index it the way ADRs are indexed: id, the assumption in one line, subject area, the observation that would falsify it. **Do not raise them yet.**

**Open design questions** — branches an earlier interview closed *deferred-later*, *blocked*, or *stable-open* — live on the project's issue tracker, not in a file (an earlier version of this skill kept an open-items record; it turns into a backlog, which the tracker already is). Ask the user, once and in one line, which tracker items touch this work, and index what they name.

Tell the user: "N assumptions and M open questions carried forward. I'll surface them when they touch something." Then say nothing more about them until they do.

**Surface an item only when a branch's topic intersects it.** This is the whole discipline. A question about transport choice has no business appearing in a data-layer design, and a skill that recites its backlog at every interview trains the user to skip that section. Relevance is the test, not recency and not urgency — a question that has been open for a year and still doesn't touch this design stays quiet.

When one does intersect, surface it with what would resolve it, and let the user decide whether this interview is the place: it can close now, stay open, or the current branch can be shaped to avoid depending on it. An assumption a branch contradicts is handled as invalidation (prune-and-regrow), and the record is corrected at capture.

**Check items against the code at ingestion.** An item whose subject no longer exists is a retirement candidate — note it, don't act on it. Same posture as a retired lexicon term.

### Lexicon ingestion

The design's vocabulary is not invented fresh each time. Scan for an existing lexicon:

- `docs/lexicon.md`, `docs/design/lexicon.md`
- `docs/glossary.md`, `GLOSSARY.md`, `LEXICON.md`
- `.claude/lexicon.md`

Load it in full — unlike ADRs, every entry is potentially in play. If it has grown past about thirty entries, or its entries describe code rather than meaning, say so in one line and offer the `design:lexicon` skill's consolidation as separate work. Don't consolidate inside the interview.

**Inherited terms are binding.** Use them exactly as defined, from the pitch recap onward. If this design needs a term the lexicon already defines differently, that is not a naming preference to resolve quietly: either the design is wrong about the concept, or the established meaning has shifted and the entry needs to change. Surface it and let the user say which.

**Check inherited terms against the code.** An inherited entry that fails the `design:lexicon` skill's tests — the name of a component, a word in its ordinary sense — is a candidate for retirement: note it, don't act on it. A term the code uses with a meaning that has drifted from its entry is worth surfacing immediately, because everything downstream will inherit the confusion.

If no lexicon exists, this is the first interview and it starts empty. Say so in one line; don't treat it as a problem.

### Where this project keeps design documentation

The three scans above answer a question beyond their own contents: **where design documentation lives in this project.** Whatever they found establishes it. ADRs under `documentation/decisions/` means design docs belong under `documentation/`; a lexicon at `.claude/lexicon.md` means this project keeps design state in `.claude/`.

Record that location. Phase 9 writes everything there, and nothing in this skill carries a path of its own — a project's documentation layout is the project's business, and a design skill that imposes one is wrong about whose repo it is.

If the scans found nothing, don't pick a location now. Capture will ask if it ever runs, and most interviews never need one.

## Phase 3: Scope recap and confirmation

Before seeding the tree, state your understanding back to the user and let them correct it. Cover:

- **What's being built or changed**, in a sentence or two, in your own words rather than theirs.
- **What it touches** — the modules, surfaces, and existing behavior the codebase scan puts in the blast radius.
- **What you're treating as out of scope**, and why. Wrong guesses here are cheap to fix now and expensive to fix after ten branches have been built on them.
- **The assumptions** you picked up in Phase 1, listed plainly. This is the user's first chance to shoot one down before the tree grows on top of it.

Also state the **change-type** you're assuming — greenfield, additive, modifying, or mixed — since it sets how hard the Phase 2 exploration has to work and which branches will matter. State it as an inference; don't put it to a vote. "Mixed" is the honest answer when signals point both ways, and most non-trivial work is mixed: an addition that touches existing code, a rewrite that preserves an interface.

Do not ask the user to classify the work. What *kind* of software this is — service, library, CLI, pipeline, UI — determines nothing about what the design needs. The properties of the work do, and those get checked in Phase 4 and rechecked throughout the walk. A confirmation turn spent ratifying a label is a turn not spent catching a wrong assumption.

## Phase 4: Tree seeding

**Before seeding anything, load the `design:design-philosophy` skill.** Its principles seed branches of their own (below), and they shape how every other branch is framed. A branch closed before they are loaded was closed without them, and reopening it later costs more than loading them now.

### Universal core branches

Always seed these. They apply to any non-trivial software design:

- **Functional scope and explicit non-goals.** What the thing does and, just as important, what it doesn't.
- **Consumers, callers, affected parties.** Who uses this. Who's affected by it changing.
- **Interface surface.** Whatever shape applies: API, CLI, library entry points, UI, event topic, RPC, config.
- **Data shape.** Inputs, outputs, invariants, and any persisted state.
- **Error and failure semantics.** What can go wrong, how it's surfaced, what's recoverable.
- **Testing strategy.** How we'll know it works and stays working.
- **Dependencies and integration points.** What this leans on; what leans on this.

### Branches implied by the properties of the work

The core branches are not enough on their own, and the rest do not reliably fall out of the pitch. Nobody derives "what does a crash halfway through leave behind" from a pitch about a sync tool; the pitch is about syncing.

So: read the *Conditions of the work* section of `references/conditions-and-patterns.md` and check every condition against this design. Each one that holds implies branches — seed them. Conditions compose freely and most non-trivial work matches several. Checking a condition that doesn't hold costs one line of thought; missing one that does costs a branch that never gets opened.

There is no taxonomy step here. Don't decide what kind of software this is in order to look up its branches — that was the old mistake, and the categories always collapse at the edges. Ask whether each property holds. A CLI that persists config across releases and a service that persists rows across deploys have the same evolution problem and want the same branch.

The check is not one-and-done. Phase 5 regularly surfaces a condition that wasn't visible from the pitch; re-run it as the tree grows.

### Branches implied by design philosophy

Seed the branches the `design:design-philosophy` principles imply for this design — loaded at the top of this phase. It is a separate skill because the same principles apply when an agent implements from a spec, not only when one is being designed; the interview needs the design-time rendering of them, which the skill carries.

Don't treat the principles as a review pass at the end. "Is this interface simpler than what it hides" and "what knowledge does this module own exclusively" are branches, opened at seeding, closed through the four locks like any other.

Branches are not exhaustive; grow more as the conversation reveals them. Prune the ones that genuinely don't apply (e.g., observability for a pure-function utility) but be willing to defend the prune; absence of a branch is itself a design choice.

## The lexicon

The interview carries two pieces of cross-branch state: the assumption nodes, and the lexicon. Both are first-class, both are surfaceable whenever the user asks, and both get laid out at wrap-up.

The lexicon is the domain's language — the words someone needs defined to talk about using or developing the system. Its job is that every branch closes in words that already mean something exact, so that the design, and anything later written from it, can't diverge on what a word meant. The code takes its names from it, not the other way round.

The `design:lexicon` skill owns what may enter it and what an entry says. Load it before the first admission; none of it is reimplemented here.

### Admission

**Terms are admitted only at branch closure, and only when closing that branch required the term to carry a specific meaning.** This is the whole convergence mechanism, so don't route around it. A lexicon whose growth is coupled to how much has been *said* never converges, because conversation doesn't. Coupled to branches closed, it does, because branches are finite and closing.

A term that closure required is admitted only if it passes the `design:lexicon` skill's admission tests. They are deliberately not repeated here: they live in that skill and change with it, and a copy here would go on being applied after it had gone stale. So a closure that might admit a word, or refuse one, is decided with the skill loaded. If `design:lexicon` has not been loaded in this conversation, load it before the recap names any term as admitted or refused.

- **A branch deciding something is not a reason to admit a word.** The decision belongs to the tree and, when ADR-worthy, to an ADR. The word is admitted only if the closure fixed what it *means*.
- **The names of components this design introduces are never admitted** — modules, types, mechanisms. They are the design's structure, recorded in the tree and then in the code, which is what anyone reads to talk about them.

### Inherited and new

Track which entries came from the ingested lexicon and which this interview added. The distinction matters at wrap-up: inherited terms belong to the codebase and outlive this design, while new ones are this interview's claim on the vocabulary and need the user's explicit sign-off before they're written back.

Inherited entries are binding whether or not they would pass the tests today; the interview doesn't re-litigate them. One that fails is noted for consolidation (Phase 2), not dropped.

**A closure amends an inherited entry only when it changes what the word means.** A decision about how the concept behaves goes to the tree and its ADR, and the entry stays as it is. An entry that grows a sentence with every decision touching its concept becomes a second, drifting description of the system.

### Size

Target roughly 20 to 30 entries, inherited and new together. Past that, adding one means arguing another out — say so out loud when it happens — and an inherited lexicon already past it needs the `design:lexicon` skill's consolidation, as separate work. A lexicon is an interface, and one with two hundred entries is a shallow module that isn't pulling its weight.

### Use

Once a term is in the lexicon, use it and only it. If a closure wants a different word for something already named, that's either a term to admit as a real distinction or a slip to correct — decide which, out loud, rather than letting both words circulate.

## Phase 5: Interview and branch closure

### Walking the tree

At each step, pick the highest-priority open branch. Priority order:
1. Branches that are foundational (other branches depend on their resolution).
2. Branches that are likely contentious or surprising.
3. Everything else.

Don't go in fixed order; reassess after each closure. Resolving a foundational branch often reframes others.

### Per-branch interview

For each branch:
1. State the branch and why it's currently open. Briefly.
2. Generate 3 to 7 probe questions specific to this branch and to what the codebase scan turned up. Probes should be concrete, not generic. "How will you handle partial writes if the downstream service times out?" beats "How will you handle errors?". When generating probes, consult `references/conditions-and-patterns.md`. It catalogues ambiguity patterns — directionality, expiry and stuck states, reversal semantics, rule precedence, identity and equality, cardinality and bounds, time, ordering and concurrency, atomicity and partial failure, evolution and compatibility, trust boundaries, failure surfacing — each with the question shapes that expose it. Match patterns to the shape of the branch and read only those sections; usually one to three apply, sometimes none. The examples in that file are drawn from deliberately varied domains and are illustrations, not questions to ask verbatim.

   Where the branch is a genuine fork — more than one workable approach exists — one probe is always "what else could this be?", asked here rather than at closure. The point is to generate the alternative while the answer is still open and it can still win. Asked after the fact it produces retroactive justification, which is worse than nothing: it makes a defaulted decision look deliberated. Don't ask it on branches that aren't forks.
3. Ask probe questions adaptively. Track answers. Track new assumptions surfaced by the user; record them as assumption nodes upstream of this branch.
4. When you think the branch is done, run the four locks (see below). Only after all four pass does the branch close.
5. Once it closes, check what closing it changed about the tree. Did the resolution imply a branch that doesn't exist yet? Did it reveal a condition of the work that wasn't visible at seeding (Phase 4)? Did it contradict a closed branch or invalidate an assumption (Phase 7)? Seeding is deliberately light, so growth during the walk is what makes the tree complete. This step is not optional.

### The four locks before closure

A branch closes only when all four pass:

1. **Probes addressed.** Every probe question has been answered, or explicitly deferred-with-reason, or marked out-of-scope-with-reason. "I'll figure it out" without a stated reason is not enough.

2. **Summary recap.** Restate the branch's resolution in your own words, in two to four sentences. Ask the user to confirm or correct. This catches drift between what the user said and what was understood.

3. **Adversarial check.** Generate one of: "What case would break this?" or "What haven't we considered here?" Ask the user. Their answer either reveals a gap (branch stays open, new probes added) or confirms robustness.

4. **Explicit close.** The user must confirm closure with words. Drifting away from the branch in conversation does NOT close it.

### Closure states

When closing, record one of these terminal states with a sentence of rationale:

- **decided** — concrete answer recorded
- **deferred-implementation** — design-level says implementation will figure it out (the design doesn't need to specify it, and a reasonable implementation can pick)
- **deferred-later** — out of this version's scope, planned for a later phase
- **out-of-scope** — irrelevant to this design
- **blocked** — needs external info or a decision elsewhere before it can close (record what's needed and from whom)
- **stable-open** — in tension with another branch, parked until that one moves

"Decided" requires the actual answer in the rationale. The others require the reason.

**Three of these are promises, not conclusions.** *deferred-later*, *blocked*, and *stable-open* all mean the question outlives this interview, so each needs the thing that lets a later one pick it up: what would resolve it. For *blocked*, what's needed and from whom. For *deferred-later*, which phase or trigger brings it back. For *stable-open*, which branch it's in tension with. Without that field the item is a note that something is unfinished, which nobody can act on.

If a branch resolves an item carried in from a prior interview, say so at closure and mark the carried item resolved.

**Every *decided* closure also records whether it was a fork.** One line, and it is one of two shapes:

- **Fork.** The alternatives that were on the table, and why each was rejected. The rejection reasons are the durable part — they're what stops the same option being re-evaluated from scratch a year later by someone who has no idea it was already ruled out.
- **No fork.** One option, and what forced it — an ADR, an existing interface, a platform constraint. This is a legitimate and common closure; it just isn't a decision in the sense that warrants a record of its own.

Don't manufacture a fork to make a closure look thorough. "No fork, forced by ADR-0012" is an honest and useful thing to write. Phase 9 reads this line directly rather than trying to infer from the rationale whether a choice ever existed.

**Lexicon admission happens here.** If closing this branch required a term to carry a specific meaning, admit it now against the `design:lexicon` skill's tests, and write its entry in that skill's shape. This is the only moment terms are admitted. Say which terms you added and why, in one line — a term entering the design's vocabulary is a small decision, not bookkeeping.

## Phase 6: Anti-cycling brakes

These prevent the interview from spiraling.

### Design-vs-implementation gate

When a probe question is really about how to write the code (variable names, internal data structure choices, exact algorithms, helper function shapes), say so explicitly and mark it as deferred-implementation. The skill is allowed and encouraged to push back: "That's an implementation decision; let's note it deferred and move on."

The line is not always crisp. Rough heuristic: if the question's answer would only matter to someone reading the code (not to anyone using the interface, depending on the behavior, or maintaining the system), it's implementation.

### Reopen cap

A branch may be reopened up to three times. After the third reopen, the underlying tension is escalated to a top-level "unresolved tension" node that must be explicitly resolved before either branch can re-close. This prevents ping-pong oscillation.

### Soft per-branch budget

If a single branch consumes a disproportionate share of the interview (rough rule: more than about a quarter of total questions asked), surface it: "We've spent a lot of time on this branch. Want to park it as stable-open, defer it, or keep going?"

## Phase 7: Contradictions and assumption invalidation

When a new answer contradicts an earlier closed branch:

1. Name the contradiction explicitly. State both sides.
2. Trace upstream: identify any assumption nodes that both branches depend on.
3. Ask: "Is X wrong, is Y wrong, or did assumption Z (made when we were discussing W) just stop holding?"
4. If a shared assumption is invalidated:
   - Mark all branches downstream of that assumption as "needs regrowth".
   - Prune them back to the assumption node.
   - Regrow with corrected understanding, walking each affected branch through the four locks again.
   - The reopen cap applies to prune-and-regrow cycles. If a branch has been regrown three times, escalate as unresolved tension.
5. If no shared-assumption issue (just one of the two answers is wrong):
   - User picks which side wins.
   - The losing branch's state moves to "revised" with a pointer to the winning resolution.
   - The winning branch closes via the four locks.

Surfacing contradictions, not auto-reopening, is deliberate. Auto-reopen interacts badly with the cycling failure mode; surfacing keeps the user in control.

## Phase 8: Wrap-up

The interview is complete when every branch is in a terminal state (decided, deferred-implementation, deferred-later, out-of-scope, blocked-with-resolution-path, or stable-open with explicit acknowledgment of the unresolved tension).

First, consolidate the lexicon. Merge entries that differ only in shading, and delete any whose definition turned out to be the ordinary meaning of the word. Drop terms this interview added that never got a second use.

**Consolidation only prunes what this interview added.** An inherited term that this design didn't happen to use is not dead — it belongs to the codebase, and other work depends on it. Never drop one as unused. If an inherited term genuinely looks retired, say so and let the user decide, or offer the `design:lexicon` skill's consolidation; that's a change to shared vocabulary, not interview housekeeping.

Then lay out the full tree in the conversation: every branch, its terminal state, and its rationale — the actual decision for anything marked decided, the reason for everything else. Include the assumption nodes and which branches hang off them, and the consolidated lexicon. Mark which decided branches are ADR-worthy — a real fork, consequences that outlive the change, and a future reader who would ask why — and flag any that supersede an ADR indexed in Phase 2. Flag them here; Phase 9 is where they get written. Then summarize: counts per terminal state, any unresolved tensions, any blocked items needing external action.

The goal is that the design is complete and present in context when the interview ends, not that it has been written somewhere. Mention once that Phase 9 can turn the tree into artifacts, and leave it there — don't generate anything unless the user asks.

Three things are worth offering explicitly, because they aren't deliverables — they're the inputs to the next interview, the same way the ADR index is:

- **The lexicon**, showing which entries are new and which changed.
- **The assumptions record**: assumptions carried in that still stand, assumptions this interview added (each with how you would know it stopped holding), and assumptions this interview invalidated, removed.
- **Tracker candidates**: one line per branch closed *deferred-later*, *blocked*, or *stable-open*, with what would resolve it, for the user to file on the project's issue tracker. Never a file in the tree.

Offer all three in one line. If the user declines, the vocabulary, the assumptions and the open questions die with the conversation and the next design starts from nothing — which is worth the one line, and is exactly the failure that makes a design skill useless on the second run. Still an offer, not an action.

## Phase 9: Capture (on request only)

The interview ends at Phase 8. This phase runs when the user asks for artifacts, and not otherwise.

Read `references/artifacts.md` first. It owns which artifacts this design needs, the provenance rules all of them follow, and what makes each one complete.

The rule that matters most: **capture is a completeness check, not a transcription step.** Artifacts need detail the tree does not always carry — exact behavior, field constraints, error codes, test cases. Where the tree has the answer, write it plainly. Where it doesn't, you are inferring, and inference gets marked and put to the user. If a section would need more inference than fact, don't write it: name the branches that were never closed and offer to reopen them. Reopening is a normal continuation of Phase 5, not a failure.

A confident document built on invented detail is worse than no document, because it gets implemented as though all of it was agreed.

## Anti-patterns to avoid

- Closing a branch without running the four locks. The locks exist precisely because Claude tends to declare things done prematurely.
- Hiding the assumption tree. The user should be able to ask "what assumptions am I making?" at any point and get a clean list.
- Treating "decided" as the only good outcome. Deferred and out-of-scope are valid and often correct. Forcing a decision when the user doesn't have one is worse than recording a deferral with rationale.
- Going down implementation rabbit holes. The design-vs-implementation gate is there to be used.
- Skipping the codebase scan or ADR index for additive or modifying work. This is the single biggest source of bad designs.
- Surfacing ADRs without the staleness flag when they're old or non-Accepted. Cargo-culting stale decisions is worse than not consulting them.
- Reaching for a category for the work — "this is a CLI, so..." — instead of checking its properties. What kind of software it is determines nothing; what it does determines everything.
- Treating the seeded branches as the whole tree. Seeding is a floor, not a ceiling. A tree that ends up as the core branches plus whatever the pitch happened to mention is a tree that missed things.
- Reciting carried-forward assumptions or tracker questions that don't touch this design. Relevance is the only trigger. A backlog read aloud at the start of every interview is a section the user learns to skip, and then the one item that mattered gets skipped with it.
- Closing a branch as *deferred-later*, *blocked*, or *stable-open* without recording what would resolve it. That field is the entire reason the item is worth carrying.
- Seeding, or closing any branch, before `design:design-philosophy` is loaded. Its principles are seed material, not a review pass; a tree grown without them has to be reopened.
- Letting the lexicon grow with the conversation instead of with closures. That is the specific failure that makes a lexicon useless: it becomes a glossary of ordinary words, and nobody reads it.
- Admitting a component's name, or growing an entry by a sentence because a decision touched its concept. The first puts the code into the lexicon, the second the decisions; either turns a lexicon of thirty terms into one of sixty.
- Writing an artifact section on inference without saying so. Marked inference is fine and often necessary; unmarked inference is the thing Phase 9 exists to prevent.
- Using constrained-option tools to ask questions. Always prose.

## Test anchor: how to know the skill is working

A run is going well if:
- The user feels their pitch was understood and not warped.
- Each branch closure has a defensible rationale, not just "yes done".
- Implementation rabbit holes get gated, not pursued.
- ADRs surface only when relevant and get flagged when stale.
- Contradictions are named clearly and resolved with assumption-tracking, not papered over.
- The final tree would be enough for a careful reader to implement from, or write up, without coming back with further questions.

A run is going badly if:
- Branches were seeded or closed before `design:design-philosophy` was loaded.
- Branches close with vague summaries.
- The user feels interrogated rather than collaborated with.
- The interview spirals on a single branch for a quarter of the conversation without parking it.
- Implementation details creep into branch resolutions.
- Assumptions made early are forgotten and not referenced when later contradictions arise.
- The final tree is the core branches plus whatever the pitch mentioned, and nothing the conditions check or the walk should have added.
- The lexicon has grown past the point of usefulness, or holds entries that restate ordinary words.
- Capture produced a complete-looking set of artifacts without ever reporting a gap.
