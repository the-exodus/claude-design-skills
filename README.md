# claude-design-skills

A [Claude Code](https://claude.ai/code) plugin marketplace with three plugins:

- **`design`**: design interviews, decision records, a project lexicon, and the structural principles behind them.
- **`implementation`**: how names and comments read, and the review a change gets before its pull request. Depends on `design`.
- **`guard`**: a hook that makes changes to a repository's protected paths, such as its architecture tests, reach the author. Required by `design-interview`'s [autonomous mode](autonomous-mode.md).

## Install

```sh
claude plugin marketplace add the-exodus/claude-design-skills
claude plugin install implementation@claude-design-skills   # brings design with it
claude plugin install guard@claude-design-skills            # optional; needs Python 3
```

For the design skills alone, install `design@claude-design-skills`. Restart Claude Code to load. To update:

```sh
claude plugin marketplace update claude-design-skills
claude plugin update design
claude plugin update implementation
claude plugin update guard
```

## `design`

### `design-interview`

Takes a rough pitch to a complete design before code is written: a tree of branches, each closed in a defined state with its rationale.

- Branches are seeded from properties of the work (does someone wait on it, does state outlive a version, are there callers you can't deploy in lockstep), not from what kind of software it is.
- A branch closes only after its probes are answered, its resolution is recapped, an adversarial question is asked, and the user confirms.
- A closure that draws a boundary also decides the architecture test that protects it.
- On request, captures the tree as a functional spec, edge cases, acceptance criteria, interface contracts, a domain model and ADRs, with inferred content marked.
- Reads and writes back the project's ADRs, lexicon and assumptions record; deferred and blocked branches go to the tracker.
- [Autonomous mode](autonomous-mode.md): runs without the author and brings one batch of questions.

### `adr`

Format and house rules for Architecture Decision Records (Nygard's Context / Decision / Consequences, with a Status): which decisions get an ADR, one decision per ADR, numbering, the index, and supersede-or-addendum instead of rewriting an Accepted record. A record whose boundary an architecture test protects says so in a fixed sentence.

### `lexicon`

Rules for a project's lexicon, the domain's language: an entry is language rather than code, needs defining, and is the one word for its concept. Consolidates a sprawling lexicon entry by entry, checks it against the code, and writes nothing until the user signs off.

### `design-philosophy`

The structural principles applied when designing and when implementing: interfaces simpler than what they hide, hiding decisions, no decomposition by time, no pass-through layers, pushing complexity down, defining errors out of existence, considering alternatives, modest generalization.

## `implementation`

### `review-cycle`

Before a pull request, fresh-context subagents review the change against its brief, each through one lens:

- **adversarial**: inputs and states that break a criterion or contract, proved with throwaway tests where possible;
- **design parity**: the code against the decision records and the brief;
- **simplification**: complexity the change added;
- **platform reality**: what the change assumes about the platform, documented, probed or recalled.

The cycle triages the findings, sweeps for each defect's whole class, fixes test-first and records forced decisions through `adr`. The brief comes from the tracker or the user, never inferred. In a repository that uses `guard`, it also traces every change to a protected path to a closure the author approved.

A repository adds lenses of its own as skills in its tree:

```yaml
disable-model-invocation: true
metadata:
  review-lens:
    applies-to: ["src/Platform/**"]   # path globs
    extends: platform-reality         # a built-in lens, or absent for a reviewer of its own
```

### `code-style`

How names and comments read, loaded before code, names or comments are written or changed. Names say what a thing is, using the lexicon's words. A comment keeps only what the code in view cannot say: a platform behaviour, a recorded decision, a caller's contract, a reason.

## `guard`

A PreToolUse hook on Edit, Write, NotebookEdit, Bash and PowerShell. In a repository with `.claude/protected-paths.txt`, a change to a listed path asks the author, and the agent records a provisional closure and stops. Without the list it does nothing. Runs on Linux, macOS and Windows (Python 3; pwsh 7 where there is no Git Bash). [Its README](plugins/guard/README.md) defines the list and how a repository opts in.

## Releasing

Each plugin is versioned and tagged on its own. Evals are described in [`evals/README.md`](evals/README.md).

```sh
claude plugin validate .
claude plugin validate ./plugins/<name>
claude plugin tag ./plugins/<name>   # creates <name>--v<version>
```
