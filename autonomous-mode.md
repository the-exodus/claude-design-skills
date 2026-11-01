# Autonomous mode

`design:design-interview` can run without the author present. It closes what the codebase, the decision records, the standing assumptions and the platform already decide, and brings the author one batch of questions for everything else.

The mode runs only when the invoking prompt asks for it. Otherwise the interview is live.

## Starting a run

The prompt asks for the autonomous mode and says where the batch goes, and later the brief, the assumptions record and the tracker candidates: an issue, a file, the conversation.

```
Run design:design-interview in autonomous mode on THE-123. Put the batch on the issue.
```

The prompt is the author's only turn before the batch. Whatever it decides counts as decided.

## What the repository needs

Before anything is seeded, the run checks the feature's **blast radius**: the modules the change touches, plus every module that shares a decided boundary with one of them. A **boundary** is what `design:adr` defines: one module's use of another, a surface and the consumers allowed to use it, or a prohibition, where a decision drew it.

| Requirement | How it is checked |
|---|---|
| The `guard` plugin is opted in: `.claude/protected-paths.txt` names itself, the architecture tests, `.claude/settings.json` and `.claude/settings.local.json`; `.claude/settings.json` enables `guard`, sets `permissions.disableBypassPermissionsMode` and `"disableAllHooks": false` | Read; see [`plugins/guard/README.md`](plugins/guard/README.md) |
| Every boundary in the blast radius is protected by an architecture test | The smallest realistic violation of each boundary, on a scratch branch, then the tests; a boundary is protected only if something fails. Without a branch: in place, on files clean against `HEAD`, each violation reverted and `git diff` checked clean. If nothing can run, by reading, and the check is reported as weaker. |
| The architecture tests are meaningful: each traceable to a decision, together complete over the blast radius, allow-lists, protected by the list | Read |
| Behaviour tests the run can use to check its own work | Read |
| Decision records with their rejected alternatives | Read |

A missing requirement is an objection: the run says what is missing, what it costs, what would fix it, recommends a live interview, and stops. The author can override; the override is recorded and does not silence later objections.

## What the run closes, and what it asks

A branch closes **decided** only when nothing else was possible: an ADR, a standing constraint, an existing interface or the platform's documentation forces it, or every alternative violates one of them. The closure quotes the text that states the answer; without a quotation it is a fork. Anything the prompt names as open is always a fork. A question about how the host behaves is answered by running something.

A branch closes **provisionally**, as an assumption the walk continues on, when:

- two or more options satisfy every constraint,
- it would supersede or add an addendum to an ADR,
- it would change an architecture test (every closure that draws a boundary does, since it decides the test that protects it),
- it changes a user-visible surface: commands, configuration, a protocol,
- it admits or amends a lexicon term,
- it rests on a standing assumption whose falsification signal cannot be checked.

Questions only someone reading the code would care about (exit codes, an interface's exact shape, units or precision inside a module) go on a list left to implementation, neither asked nor counted.

Before the batch, two reviewer subagents always read the work: a **blind** one, which checks that each decided closure's quotation states its answer and re-derives it from the question alone, and an **adversarial** one, over the whole tree. A decided closure that fails either becomes a fork and is marked *close call*.

## The batch

1. The scope recap, then one line: `Forks: N genuine.`
2. The provisional items, `P1`, `P2`, …, one decision each, ordered by how much of the tree hangs on it. Each gives the question, the recommendation, the rejected alternatives and why, the branches that regrow if it is rejected, and the protected paths it would change. Each is marked:
   - *fork*: the choice is open, including any item that offers options;
   - *forced*: the answer is settled, and a rule (a supersede, an architecture-test change, a surface, a lexicon term) makes it provisional;
   - *close call*, as well, where a reviewer disagreed.
3. The appendix: each decided closure with its grounds quoted, the branches parked, the assumptions added or invalidated, any override.
4. What is left to implementation.

Confirming an item costs a word. A rejected item is an invalidated assumption: the branches on it are pruned and regrown.

## When the run stops

- **The repository is unsuited** to the mode for this feature: see above.
- **The feature is unsuited:** more than seven genuine forks, or the author's answers regrow new provisional items more than once. The run recommends a live interview and hands over the tree so far. *Forced* items do not count toward this.

## After the batch

With the author's answers in, the run regrows what was rejected and capture always runs: the decision records, the lexicon and assumptions record, and the brief, where the prompt said.

During the build, an edit to a protected path stops at the `guard` hook, since the design did not decide it: the agent records a provisional closure naming the path and stops for the author. Before the pull request, `implementation:review-cycle` traces every protected change in the diff to a closure the author approved, lists them in its closing comment, and reports an untraced change as `Protected change without an approved closure: <path>`.

## Gaps

A script that writes a file itself, a nested `claude` started with its own `--settings`, and `claude --bare` get past the hook. The review cycle's trace is the backstop for all three.
