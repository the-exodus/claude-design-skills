# claude-design-skills

Skills for [Claude Code](https://claude.ai/code) for designing software and for making the code, packaged as a plugin marketplace with two plugins:

- **`design`**: what design work needs, whenever it comes up — design interviews, decision records, a project lexicon, and the structural principles behind them.
- **`implementation`**: how the code gets made — how names and comments read, and the review cycle a change goes through before its pull request. It depends on `design` and uses its skills; `design` never depends on it.

## Install

```sh
claude plugin marketplace add the-exodus/claude-design-skills
claude plugin install implementation@claude-design-skills
```

Installing `implementation` installs `design` with it, since `implementation` declares it as a dependency (`>=0.7.0`): Claude Code installs and enables a plugin's dependencies at the same scope, from the same marketplace, and the success message lists them. To have only the design skills, install `design@claude-design-skills` on its own instead.

Restart Claude Code to load. To pick up changes pushed since:

```sh
claude plugin marketplace update claude-design-skills
claude plugin update design
claude plugin update implementation
```

## What's in it

### The `design` plugin

#### `design-interview`

Takes a rough pitch to a complete design before any code is written, as a tree of branches each closed in a defined terminal state with rationale.

- **No taxonomy.** Branches are seeded from *properties of the work* — does a person wait on it, does state outlive a version, are there callers you can't deploy in lockstep — not from what kind of software it is.
- **Four locks before any branch closes:** probes addressed, summary recap, adversarial check, explicit confirmation from the user.
- **Anti-cycling brakes:** a design-vs-implementation gate, a reopen cap, and a per-branch budget, because the failure modes of premature closure and runaway depth are opposed and both real.
- **Capture on request** into a functional spec, edge cases, acceptance criteria, interface contracts, a domain model, and ADRs — with provenance, so decided and inferred content never look alike.

Three things persist across a project's lifetime and are read back at the start of every interview:

| | in | out |
|---|---|---|
| **ADRs** | indexed, surfaced when relevant, rejected options included | written via the `adr` skill, with supersession |
| **Lexicon** | loaded in full, binding, checked against the code | admitted by the `lexicon` skill's tests, consolidated and written back |
| **Assumptions** | indexed, surfaced *only* on topical relevance; open design questions come from the tracker | standing assumptions with how you would know each stopped holding, plus measured facts; deferred, blocked and stable-open branches go to the tracker as candidates |

#### `adr`

House rules and format for Architecture Decision Records — Michael Nygard's Context / Decision / Consequences, with a Status. Owns which decisions get an ADR, one decision per ADR, numbering, the index table, and the rule that an Accepted ADR is **never rewritten**: a changed decision is superseded, anything else is a dated addendum. `design-interview` hands ADR writing to this skill rather than carrying a competing format.

Ships with a worked example set: an Accepted ADR with an addendum, a superseded ADR and the ADR that supersedes it, a rejected proposal, and the index listing all four.

#### `lexicon`

House rules for a project's lexicon — the domain's language, in the DDD sense — and the procedure for bringing a sprawling one back. Three tests, applied in order, decide what may be an entry: **it is language, not code** (it would survive a rewrite with a different decomposition), **it needs defining** (overloaded, narrower than ordinary use, or a distinction that must not be conflated), and **it is the one word for its concept**. An entry states what the word means and what it is distinct from; behaviour belongs to the decision records, and the names of components belong to the code, which takes its names from the lexicon rather than the other way round.

Consolidation applies the same tests to every entry of an existing lexicon — retire, reframe, merge, rewrite or keep — checks the survivors against the code for drift, accounts for every sentence it cuts, and writes nothing until the user signs off. `design-interview` loads it for admission.

#### `design-philosophy`

The principles the interview seeds branches from, and that apply again when implementing from a spec: complexity as the thing to minimize, interfaces simpler than implementations, hiding decisions rather than just code, not decomposing by time, no pass-through layers, pushing complexity down rather than out, defining errors out of existence, considering alternatives before committing, long-term simplicity over short-term speed, and modest generalization.

Separate from the interview because the same principles apply when there's no interview — an agent implementing from a prompt still makes structural decisions.

### The `implementation` plugin

#### `review-cycle`

The review a change gets before its pull request goes up, so that less is left for anyone reviewing the PR. Subagents that have not seen the conversation that produced the change each review it through one lens, against the brief it was asked to fulfil:

- **adversarial** — inputs, orderings and states that break an acceptance criterion or a contract, including contracts whose meaning the change altered; proved with throwaway tests where it can.
- **design parity** — the code against the recorded decisions, the documents against the code, behaviour the brief never asked for, and a brief that contradicts itself; a records-only mode for changes with no code.
- **simplification** — complexity the change added that `design-philosophy` would not, at most five findings, each cheaper than what it replaces.
- **platform reality** — what the change assumes about the platform, runtime or outside services, classified as documented, probed or recalled.

Lenses are chosen by what the change does, not by its paths. The cycle then triages what the reviewers found, searches the repository for each defect's whole class, fixes test-first, records forced decisions through `adr`, and re-runs a lens after large fixes. Context comes from what the repository already has — its agent instructions, README and build files — and the brief from the tracker those name, or from the user; the cycle never reviews against a brief it inferred.

A repository adds knowledge of its own as **review lenses**: ordinary skills in its own tree that declare themselves in frontmatter and never load in an ordinary session.

```yaml
disable-model-invocation: true
metadata:
  review-lens:
    applies-to: ["src/Platform/**"]   # path globs
    extends: platform-reality         # a built-in lens, or absent for a lens of its own
```

A lens that extends a built-in one is appended to that reviewer's brief; one of its own gets a reviewer of its own. Either way its body reaches the reviewer word for word.

#### `code-style`

How names and comments read, loaded before any code, name or comment is written or changed — renames and comment passes included. Two principles: *name it what it is, call it what it does*, with domain words taken from the project's lexicon; and *comments express what the code can't, and only that*.

Comments are judged clause by clause, and locality is the test. A clause the name, the signature or the code in view already says goes; a clause that carries context from elsewhere — a platform behaviour, a recorded decision, an invariant another type holds, a caller's contract, a reason — stays; a comment with both is shrunk. Keeping is the common case, and keeping is not encouraging: a comment is written only when it carries something from elsewhere. Because a cut clause can quietly break the sentence left behind, every shrink is re-read on its own. A citation never stands in for a claim, cites by number, and follows the project's convention for where citations may appear.

## Layout

```
.claude-plugin/marketplace.json
plugins/design/
  .claude-plugin/plugin.json
  skills/design-interview/
  skills/design-philosophy/
  skills/adr/
  skills/lexicon/
plugins/implementation/
  .claude-plugin/plugin.json      # depends on design >=0.7.0
  skills/review-cycle/
  skills/code-style/
evals/                            # the plugins' eval suite; not shipped
```

## Releasing

Each plugin is released on its own; tag the one whose version changed.

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none   # see evals/README.md
claude plugin validate .
claude plugin validate ./plugins/design
claude plugin validate ./plugins/implementation
claude plugin tag ./plugins/design           # creates design--v<version>, checks manifests agree
claude plugin tag ./plugins/implementation   # creates implementation--v<version>
```
