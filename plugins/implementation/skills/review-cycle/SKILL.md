---
name: review-cycle
description: >
  The pre-PR review cycle: fresh-context reviewers by lens (adversarial,
  design parity, simplification, platform reality, and lenses the repository
  adds as skills of its own), then triage, fix, record and re-run. Load when a
  branch is ready for its pull request, when asked to review your own branch
  or an issue's work before it goes up, or when the user invokes
  /review-cycle. NOT for reviewing a pull request someone else opened, and NOT
  a substitute for running the build and the tests.
---

# Review cycle

Before a change goes up as a pull request, subagents that have not seen the
conversation that produced it review it, each through one lens. This skill is
that step: it chooses the lenses, briefs the reviewers, and says what to do with
what they find. It runs before the PR, so that less is left for anyone reviewing
the PR.

## Inputs

- **The brief:** what the change was asked to do — the issue text, the
  behaviour wanted, its acceptance criteria and edge cases. Find where briefs
  live from the repository's agent instructions (`CLAUDE.md`, `AGENTS.md` and
  the like): if they name an issue tracker and how issues are named, fetch the
  issue, with its comments, from the argument or the branch name. Otherwise the
  brief is the invocation's argument or what the conversation gave. **If there
  is no brief, ask for it and stop.** Never review against a brief inferred
  from the commits, the code or the branch name. In autonomous mode, the batch
  of provisional closures with the author's answers is part of the brief.
- **The base:** the remote's default branch (`git symbolic-ref --short
  refs/remotes/origin/HEAD`), else the base branch the agent instructions name,
  else ask. Never assume `main`.
- **The change:** `git diff <base>...HEAD --stat` and `git diff <base>...HEAD`.
- **Lenses**, optionally, as a second argument (`adversarial,design-parity`);
  otherwise chosen by the signals below.
- Invocation arguments: `$ARGUMENTS`.

## Lenses

Each built-in lens is a brief in `references/`, passed to its reviewer verbatim.

| Lens | Brief | Finds |
|---|---|---|
| Adversarial | `references/adversarial.md` | Inputs, orderings and states that break an acceptance criterion or a contract, ripple included; may prove it with a throwaway test |
| Design parity | `references/design-parity.md` | Code against recorded decisions, documents that no longer describe the code, decisions the build forced with no record, behaviour the brief did not ask for, a brief that contradicts itself; a records-only mode for changes with no code |
| Simplification | `references/simplification.md` | Complexity the change added that the design philosophy would not; at most five findings, each cheaper than what it replaces |
| Platform reality | `references/platform-reality.md` | An assumption about a platform, runtime, library or external service that neither its documentation nor a probe supports |

Which to run, by what the change does. The rows add up: a change matching
several runs the union.

| Signal | Lenses |
|---|---|
| Records only: nothing but documents, decisions and the like changed, no code and no tests | Design parity, in its records-only mode |
| A fix, or a change inside one module that adds no interface surface | Adversarial, design parity |
| A feature, a new module, a change to a contract other code relies on | Adversarial, design parity |
| The change adds interface surface (a public type, method, parameter or command), or review fixes have grown one method across rounds | Add simplification |
| The change touches something the repository's assumptions record covers | Add platform reality |

The table is the whole selection: no lens is added or dropped on judgement,
however relevant it looks. Only the lens argument and matching repository
lenses change it. The lens argument overrides the table in both directions;
step 8 reports a lens the table would have chosen and the argument left out.

### Repository lenses

A repository adds lenses as skills in its own tree. They carry
`disable-model-invocation: true`, so they never load in an ordinary session,
and declare themselves in frontmatter:

```yaml
metadata:
  review-lens:
    applies-to: ["src/Platform/**"]   # path globs, required
    extends: adversarial              # a built-in lens, or absent for a lens of its own
```

Find them by reading the files, not through the skill listing, which does not
show `metadata`: Glob `.claude/skills/*/SKILL.md` in the repository and read
each one's frontmatter. A repository lens is selected when any changed path
matches one of its `applies-to` globs.

- **One that `extends` a built-in lens** goes to that lens's reviewer: its body
  follows the built-in brief in the same prompt. Selecting it selects the lens
  it extends, even where the table would not have.
- **One of its own** gets a reviewer of its own, briefed with the context block
  and its body.

Either way the body is passed verbatim, from the line after the frontmatter. No
reviewer is ever briefed ad hoc: what a reviewer is told is the context block
and lens bodies, nothing else.

## Procedure

1. **Gather the context block** once, and give every reviewer the same one.
   Build it from what the repository already has, not from a review-specific
   file: its agent instructions, README and build files. It holds the
   repository path, the branch and the base; the brief, verbatim, including
   comments that correct it; the acceptance criteria; how to build and run the
   tests; the conventions the instructions state; where the decisions, the
   lexicon, the assumptions record and the user references live, if they
   exist; and the decision records the change touches, by number and title. Do
   not summarise the diff: reviewers read it themselves.

   **1b. Trace protected changes.** The cycle does this itself, in every mode,
   records-only included; it is not a lens, and no lens argument drops it. It
   runs when `.claude/protected-paths.txt` exists at the base or at HEAD; with
   neither, the repository has not opted in. Its format is defined in the
   `guard` plugin's README: one git pathspec per line, `#` comments. Take the
   entries of both versions together, so that the change cannot unprotect a
   path by editing the list, and list the protected changes with
   `git diff --no-renames --name-only <base>...HEAD -- ':(glob,icase)<entry>' …`,
   one pathspec per entry. A protected change is traced when a closure in the
   brief that the author **approved** names its path or a glob covering it; a
   closure that was declined or never answered traces nothing. Each untraced
   change is a finding, written exactly `Protected change without an approved
   closure: <path>`, the path after the colon, wherever it appears, so that a
   search finds it. It holds without triage, and its disposition is **needs the
   author**: revert the change, or record a closure that names it and stop for
   the author's answer. Never record the approval yourself.

2. **Launch the reviewers in parallel**, one `Agent` call each in one response,
   `subagent_type: general-purpose`, never `fork`: a reviewer must not inherit
   this conversation. Reviewers run on the session's model; when the session
   runs on Fable, pass `model: opus` instead. Each prompt is the context block,
   then the lens brief verbatim, then the bodies of the repository lenses that
   extend it. When design parity runs in its records-only mode, put
   `Mode: records-only` at the top of its brief. Every brief tells the reviewer
   what to run, to report findings only, ranked, each marked `[defect]` or
   `[nit]`, with `file:line`, what is wrong and a concrete fix, to say what it
   checked and found sound, and not to edit files (the adversarial reviewer may
   add throwaway tests, nothing else). Wait for every reviewer's report before
   triage. Reviewers may run in the background: do not end your turn while one
   is still running, here or at step 7. Anything you start to hold the turn
   open, such as a background `sleep`, is stopped or finished before the
   report, so that the report is the last thing you say.

3. **Triage.** For each finding, decide: holds, or rejected with a reason. A
   finding holds when it names a defect, a missed criterion, a broken contract,
   a document that is now wrong, behaviour the brief did not ask for, or a
   simplification that removes more than it adds. It is rejected when it
   expands scope, restates a deliberate choice without new information, or
   trades one complexity for another. Overlap between lenses is expected; merge
   duplicates.

4. **Sweep for the class.** For each finding that holds, state the defect as a
   pattern (the same misuse, the same wrong bound, the same missing check) and
   search the repository for it, inside the change and outside it. Each hit is
   a finding of its own.

5. **Sort what is outside the brief's scope.** A defect inside the scope (the
   behaviour the brief is about, or a promise the change makes) is fixed in this
   change, whatever its size. For one outside it, follow the repository's own
   policy where its agent instructions or project memory state one. Otherwise:
   - **minor and mechanical** (no behaviour change, no design decision, nothing
     a decision record would hold): fix it in this change and prove it;
   - **needs design, is large, or changes behaviour:** a follow-up, filed where
     the brief lives with the reviewer's evidence, or listed in the report when
     there is no tracker;
   - **unsure which:** describe its size to the user and ask.

6. **Fix what holds, test-first.** A defect gets a failing test before the
   fix (a red throwaway test from the adversarial reviewer is promoted into the
   suite under a proper name, or rewritten; the rest of its files are deleted).
   A document is rewritten to describe the system as built. A decision the
   build forced gets a decision record through `design:adr`. Run the whole
   suite before committing.

   If the user asked to stop after triage, do not fix: go to step 8 and give
   each finding the disposition you would act on.

7. **Re-run once** after large fixes: one fresh reviewer, the lens whose
   findings drove the fixes, with the same context block and the same mode
   line. Its findings go through steps 3 to 6 before the report. Small fixes
   need no second round.

8. **Record and report.** Record on the brief, where the brief lives in a
   tracker, as one comment: what was fixed, what was rejected and why, what was
   left as a follow-up, one line each. When step 1b ran, the comment has a
   "Protected changes" section: one line per protected change, its path then
   the closure id it traces to or the approval quoted, or else its finding's
   exact words. Then report
   in the conversation: the findings, ranked, each with its disposition (fixed,
   rejected with the reason, follow-up, or needs the author), the "Protected
   changes" section too where there is no tracker, and, when the lens argument
   left out a lens the table would have chosen, which and why. Then hand back
   to the PR step.
