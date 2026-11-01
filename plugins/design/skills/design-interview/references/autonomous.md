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

## The design: three designers, compared

You do not walk the tree and judge your own closures. After the scope recap, independent designers each design the feature, and a comparison decides what is settled and what goes to the author. Where independent designs agree on an answer the records state, the answer is settled; where they disagree, it is the author's choice. A single designer's judgement of what is forced is not trusted on its own.

**1. Three designers**, launched in one response, each a fresh general-purpose subagent, never a fork of this conversation, none seeing another's work. Give each the invoking prompt, the scope recap, the Phase 2 findings (the records, the lexicon, the assumptions, the suitability check's result), and one stance: *the smallest change*; *the most conventional for this codebase*; *the easiest to test*. Each designs the whole feature as a tree: the branches Phase 4 seeds (the core branches, the conditions of the work in `references/conditions-and-patterns.md`, and the branches `design:design-philosophy` implies), and any it finds on the way. Each branch is closed with its answer and the text that states it, quoted word for word (an ADR sentence, `file:line`, a documentation passage, the prompt's own phrase), or left open with the designer's recommendation and the alternatives. Restatements of the prompt and pure implementation detail are not branches. Questions about how the host behaves are answered by running something.

**2. The comparison**, by a fresh subagent given the prompt, the repository and the three trees. It aligns them question by question, merging the same question asked in different words, and drops restatements and pure implementation detail; anything a user, an operator or a caller sees (exit status, a file's format, a message) is not implementation detail. Each question is then:

- **agreed, grounded**: the same answer in all three, and a quotation that states it and rules out the alternatives, checked against the text. Closed decided.
- **agreed, ungrounded**: the same answer, but nothing quoted forces it. Goes on the spot-check list, never into the design as settled.
- **divergent**: different answers, or one design decides what another asks or defers. A batch item, with each design's position and rationale.
- **rejected**: an answer that breaks a constraint the comparer can point to. Recorded with the constraint.

The comparer never picks a winner and never votes. It may add one recommendation per batch item, marked as its own. It notes where one item's answer constrains another's ("if P3 is b, P8 is moot"), and ranks the items by how much depends on them. A difference that is purely additive (one design covers a case the others missed, nothing conflicts) is merged only when it fills a gap in something already required; any other addition is listed as optional.

**3. An adversarial reviewer**, a fresh subagent over the comparison: what case breaks the agreed design, what none of the designs saw, and what no test can judge (whether the modules are deep, whether each interface is simpler than what it hides). A gap it finds is a batch item.

**Anything the invoking prompt names as open, undecided or unknown is a batch item**, whatever the designs did with it. **Provisional by rule:** an agreed answer still needs the author's word when it supersedes or adds an addendum to an ADR, changes an architecture test (every closure that draws a boundary does, since it decides the test that protects it), changes a user-visible surface, or admits or amends a lexicon term; it goes in the batch marked *forced*, with the rule. **Stale grounds:** an answer resting on a standing assumption whose falsification signal nothing here can check is not grounded.

Each settled or provisional answer is an assumption node in the tree; the author rejecting one later is ordinary Phase 7 invalidation: prune and regrow.

## Phases with the author absent

- **Phase 1.** The invoking prompt is the pitch.
- **Phase 2.** Query the tracker yourself when a connector is available; otherwise say none was reachable. Ask nothing.
- **Phase 3.** The scope recap is the batch's first item. Go on without waiting.
- **Phases 4 to 7** are the designers', the comparer's and the reviewer's work above; the four locks are replaced by it, and explicit close applies only through the author's answers to the batch.
- **Phase 8.** Instead of the offer, write the batch (below), lay out the agreed design in your reply, and end the run there.
- **Phase 9** always runs once the author has answered, since implementation follows; it writes the assumptions record and the tracker candidates where the prompt says.

## The batch

Wherever the invoking prompt puts it. The batch with the author's answers is the record of every provisional closure. In order:

1. **The scope recap**, as Phase 3 states it, then the count on one line, exactly in this form:

   > Divergent: N substantive.

2. **The items**, each headed by its id, `P1`, `P2`, …, in the comparer's order: the question; each design's position in a line, with its rationale; the comparer's recommendation, marked as its own; what in the repository bears on it; which items depend on it; and any protected path or record it would change. Mark each *divergent*, *open in the prompt*, *forced* (with the rule) or *gap* (from the reviewer). N counts the divergent, open-in-the-prompt and gap items.
3. **Spot-check**: the agreed but ungrounded answers, one line each, for the author to confirm or reopen.
4. **Appendix**: each grounded agreement with its quotation; rejected answers and the constraint; optional additions; the assumptions added or invalidated; any override of an objection.

## When the feature is unsuited to this mode

If there are more than twelve substantive divergent items, or if, after the author's answers, regrowth produces new provisional items more than once, stop. Say so first in your reply, recommend in so many words a live interview for this feature, and hand over the comparison where the batch would have gone. Write no brief.
