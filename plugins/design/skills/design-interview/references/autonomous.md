# Autonomous mode

The interview without the author present. You close what the codebase, the decision records, the standing assumptions and the platform already decide, and bring the author one short batch for everything else. The author's time is the scarce resource; yours is not.

This mode runs only when the invoking prompt asks for it. Everything in `SKILL.md` still applies except where this file says otherwise; `SKILL.md` points here at each place the modes differ.

The invoking prompt is the author's only turn before the batch. What it decides, the author decided; a decision of the prompt's that contradicts a record or a constraint is surfaced like any other contradiction. Where the batch goes, and later the brief, the assumptions record and the tracker candidates, is the prompt's to say: put each where it says, and nowhere it does not.

## Suitability check

Run at the end of Phase 2, before the scope recap and before anything is seeded. Maintaining a sound design is non-negotiable in this mode, and your own judgement is not enough to guarantee it: the boundaries the feature touches must be protected by architecture tests that fail when they are crossed.

**The blast radius** is Phase 3's "what it touches", plus every module sharing a decided boundary with one of those: a record, or a rule that cites one, draws the boundary between the two. Two modules merely listed in the same rule or table do not share one. Not the import neighbours alone, which miss a prohibition on something nothing imports yet; not the transitive closure, which grows to the whole repository. A boundary elsewhere in the repository is not this feature's concern, however weak.

**The boundaries in it** are what the `design:adr` skill says a boundary is. A record whose Decision claims "The architecture tests enforce this boundary." is a claim to verify. For a record without that sentence, ask whether a structural rule could see what it decided; if so it is a boundary too. Dependencies nobody decided are not boundaries; ignore them.

**Check, in order:**

1. **The guard.** Read, without tripping it: the protected-paths list `.claude/protected-paths.txt` exists (what its entries match is defined in the `guard` plugin's README; no list means the repository has not opted in); it names itself, the architecture-test locations, `.claude/settings.json` and `.claude/settings.local.json`; and `.claude/settings.json` sets `permissions.disableBypassPermissionsMode`, enables the plugin `guard`, and sets `"disableAllHooks": false`.
2. **The violation probe.** For each boundary in the blast radius, on a scratch branch, introduce the smallest realistic violation (the import the record forbids, say) and run the architecture tests. A boundary is protected only if something fails; reading the test and judging that it would is not the check. Only where no branch can be made, make the violation in place with your edit tool, and only in a file that is clean against `HEAD`; revert each violation before the next, and check that `git diff` is clean afterwards. If the repository cannot be built or run here, map tests to boundaries by reading, and say the check was weaker.

   A boundary this feature itself moves, by superseding or amending its record, is not a gap here: the closure that moves it is provisional and decides the test that protects the new one.
3. **The tests are meaningful.** Each protects a boundary a record names (housekeeping checks do not count); together they cover every boundary in the blast radius, not only the outermost layer; they are allow-lists, so a new dependency fails by default; and they are protected, by the list above.
4. **Behaviour tests** you can run to verify your own work, and **recorded decisions with their rejected alternatives**: without those almost nothing closes as "no fork", and the batch becomes the whole interview.

A blast radius with little established architecture is unsuited, not a reason to lean harder on `design:design-philosophy`: its decisions are the ones that establish boundaries, which is where the author's judgement is needed.

**On any failure, object and stop.** The objection is the first thing in your reply, not a caveat after a recap: which boundaries or properties are missing (each unprotected boundary by its record), what each costs this mode, what would fix it, and a recommendation, in so many words, to run this interview live, even when the fix looks small: whether to fix and rerun instead is the author's call. Write it where the batch would have gone as well. Seed nothing. The author may override explicitly; an override is recorded in the tree as an assumption node and does not silence later objections.

## Closure authority

Close a branch **decided** on your own only when there is no fork (an ADR, a standing constraint, an existing interface or the platform's documentation forces it), or when every rejected alternative violates one of those. **Quote the grounds:** the ADR sentence, the `file:line`, the documentation passage or the pitch's phrase that states the answer, word for word. "Follows from", "simpler", "the house style", "design philosophy", "the cost we already accept" or your own reasoning are not grounds. If you cannot quote something that states the answer, it is not decided: it is a fork. Two runs could close it differently, and the author has to choose.

**Anything the invoking prompt names as open, undecided or unknown is a fork.** Never close it decided, defer it or mark it *forced*, however strong the evidence looks; a fact you found that bears on it goes into the item as the recommendation's grounds.

**A restatement is not a closure.** The scope, the consumers, what the pitch already decided, how this mode works: none of it is a branch to close or count. Implementation detail is not one either (below).

Close it **provisionally** when:

- two or more options satisfy every constraint (a genuine fork);
- the closure would supersede an ADR or add an addendum to one;
- it would change an architecture test (so every closure that draws a boundary, since it decides the test that protects it);
- it changes a user-visible surface: commands, configuration, a protocol, anything a user's files or scripts depend on;
- it admits or amends a lexicon term.

**Labels follow the alternatives.** A closure that offers the author options (an addendum or a supersede, a partial or a full supersede, (a)/(b)/(c)) is a *fork*, whatever rule also applies to it. A closure a reviewer dissented from is provisional.

A provisional closure is an assumption node: record your recommended answer, the rejected alternatives and why, and walk on top of it. The author rejecting it later is ordinary Phase 7 invalidation: prune and regrow.

**Stale grounds.** Before closing on a standing assumption, check the signal its record says would show it stopped holding, wherever the code, the records or the host can answer. If nothing here can, a closure that depends on it is provisional.

## The four locks

1. **Probes** are answered from the code, the records and, where the question is how the platform or host behaves, by running something that asks it (`python3 -c …`, a command's own output). A question about the host is not a question for the author until that has been tried.
2. **The recap** is written into the tree.
3. **The adversarial check** is two fresh-context reviewer subagents, run after the walk and before the batch, each a general-purpose agent and never a fork of this conversation. They are not optional, and no run writes a batch without both:
   - **Blind**, first. Give it the pitch, the Phase 2 context, and your decided closures as question plus quoted grounds only, not your answers or your tree. For each, it checks whether the quoted text states the answer, and lists the options and which constraint rules out each; it also seeds its own tree.
   - **Adversarial**, then, over your whole tree: what case breaks it, what is missing, which grounds fail, and what no test can judge: whether the modules are deep, whether each interface is simpler than what it hides.

   A branch they find missing is seeded and walked. A decided closure whose quoted grounds do not state the answer, or whose re-derivation diverges from yours, becomes a *fork* and is marked *close call*. A finding you dispute goes in the batch with both positions.
4. **Explicit close** applies only to provisional closures, through the author's answers to the batch.

## Phases with the author absent

- **Phase 1.** The invoking prompt is the pitch.
- **Phase 2.** Query the tracker yourself when a connector is available; otherwise say none was reachable. Ask nothing.
- **Phase 3.** The scope recap is the batch's first item. Go on without waiting.
- **Phase 6.** A branch that hits the reopen cap becomes a batch item. A branch over its budget is parked *stable-open* and listed in the appendix.
- **Phase 7.** A contradiction the evidence settles, you prune and regrow yourself. Picking a side without evidence is provisional.
- **Phase 8.** Instead of the offer, write the batch (below), lay out the tree in your reply, and end the run there.
- **Phase 9** always runs once the author has answered, since implementation follows; it writes the assumptions record and the tracker candidates where the prompt says.

## The batch

Wherever the invoking prompt puts it. The batch with the author's answers is the record of every provisional closure. In order:

1. **The scope recap**, as Phase 3 states it.
2. **The provisional items**, each headed by its id, `P1`, `P2`, …, ordered by how much of the tree hangs on each. Each gives the question, your recommendation, the rejected alternatives and why, and which branches regrow if the author rejects it. One that changes a protected path or a record names those paths. Mark each item's kind up front: *fork* when two or more options satisfy every constraint and the choice is open, even if a rule would also make it provisional; *forced* when the answer is settled (by the pitch, a record or a constraint) and only a rule makes it provisional (a supersede or addendum, a changed architecture test, a surface, a lexicon term), saying which rule; alternatives you raise against the author's own decision do not make it a fork. Add *close call* when a reviewer disagreed or a re-derivation diverged. One decision per item, both ways: never fold several into one item, never split one across several. Write each so that confirming it costs a word.
3. **The appendix**: one line per decided closure with its grounds quoted; the branches parked *stable-open*; the assumptions this interview added or invalidated; any override of an objection.
4. **Left to implementation**: a plain list, outside the tree, of what only someone reading the code would care about (exit codes, fsync, an interface's exact shape, units or precision inside a module, a file's format marker, where a helper lives). Neither asked nor counted. A question the author named as open never goes here.

Right after the scope recap, state the count on one line, exactly in this form:

> Forks: N genuine.

N counts the *fork* items. Items marked *forced* still need the author's word but do not count.

## When the feature is unsuited to this mode

If there are more than seven genuine forks, or if, after the author's answers, regrowth produces new provisional items more than once, stop. Say so first in your reply, recommend in so many words a live interview for this feature, and hand over the tree so far where the batch would have gone: the count line, every branch with its state, and the provisional closures numbered `P1`, `P2`, … and marked as they would have been. Write no brief.
