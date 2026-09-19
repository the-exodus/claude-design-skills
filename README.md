# claude-design-skills

Software design and architecture skills for [Claude Code](https://claude.ai/code), packaged as a plugin marketplace.

## Install

```sh
claude plugin marketplace add the-exodus/claude-design-skills
claude plugin install design@claude-design-skills
```

Restart Claude Code to load. To pick up changes pushed since:

```sh
claude plugin marketplace update claude-design-skills
claude plugin update design
```

## What's in it

### `design-interview`

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

### `adr`

House rules and format for Architecture Decision Records — Michael Nygard's Context / Decision / Consequences, with a Status. Owns numbering, the index table, and the rule that ADRs are **superseded rather than edited**, including partial supersedes and the split that falls out of one. `design-interview` hands ADR writing to this skill rather than carrying a competing format.

Ships with a worked example set: one ADR holding two decisions, the two it split into when only one of them changed, and the index listing all three.

### `lexicon`

House rules for a project's lexicon — the domain's language, in the DDD sense — and the procedure for bringing a sprawling one back. Three tests, applied in order, decide what may be an entry: **it is language, not code** (it would survive a rewrite with a different decomposition), **it needs defining** (overloaded, narrower than ordinary use, or a distinction that must not be conflated), and **it is the one word for its concept**. An entry states what the word means and what it is distinct from; behaviour belongs to the decision records, and the names of components belong to the code, which takes its names from the lexicon rather than the other way round.

Consolidation applies the same tests to every entry of an existing lexicon — retire, reframe, merge, rewrite or keep — checks the survivors against the code for drift, accounts for every sentence it cuts, and writes nothing until the user signs off. `design-interview` loads it for admission.

### `design-philosophy`

The principles the interview seeds branches from, and that apply again when implementing from a spec: complexity as the thing to minimize, interfaces simpler than implementations, hiding decisions rather than just code, no pass-through layers, pushing complexity down rather than out, considering alternatives before committing, long-term simplicity over short-term speed, and modest generalization.

Separate from the interview because the same principles apply when there's no interview — an agent implementing from a prompt still makes structural decisions.

## Layout

```
.claude-plugin/marketplace.json
plugins/design/
  .claude-plugin/plugin.json
  skills/design-interview/
  skills/design-philosophy/
  skills/adr/
  skills/lexicon/
evals/                    # the plugin's eval suite; not shipped
```

## Releasing

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5   # see evals/README.md
claude plugin validate .
claude plugin validate ./plugins/design
claude plugin tag ./plugins/design   # creates design--v<version>, checks manifests agree
```
