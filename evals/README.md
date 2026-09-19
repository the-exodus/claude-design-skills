# Evals

The design plugin's eval suite, run with Claude Code's own runner, [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). It lives at the repo root rather than inside `plugins/design/`, so it never ships with the plugin: the marketplace installs `./plugins/design` and nothing outside it.

## Run

From the repo root:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none
```

The repo root has no `plugin.json`; each case names the plugin under test itself, with `plugins: ["../../plugins/design"]` in its frontmatter. `--eval-dir` can't do this, since it only accepts a directory below the plugin.

Results land in `evals/results/<timestamp>/` (`aggregate-result.json`, `report.html`), which is gitignored. The command exits 0 when every case meets `--threshold` (default 1.0), 1 when one doesn't, 2 on a partial run.

To iterate on one case cheaply, run it once, then confirm at the default three runs before trusting the change:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --case <case-name> --runs 1 --ablation none
```

`--tag smoke` runs only the smoke cases; `-j 4` runs four agent runs at once against the same rate limit.

The lexicon fixture cases copy a project into the workspace and rewrite its lexicon, so they need two more flags, and without them they score 0:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --tag fixture --scaffold --allow-tools Write Edit
```

`--scaffold` runs each case's `scaffold.sh` as you, outside the sandbox; it only copies the case's `fixture/` into the workspace. `--allow-tools` applies to every case in the run, so pass it with `--tag fixture` rather than on a smoke run. No case needs Bash, so the sandbox backend (`bubblewrap` and `socat`) is not required.

## Pinned settings

| Setting | Value | Why |
|---|---|---|
| `--model` | `claude-opus-5` | The skills are used from Opus sessions, and whether a skill triggers depends on the model, so the agent under test is the model they actually meet. Pinned so a model rollout isn't read as a plugin regression. |
| `--judge-model` | `claude-opus-5` | The default judge is a small fast model; the rubrics here ask for design judgement. |
| `--ablation` | `none` | The no-plugin baseline arm would double the runs, and for the current cases it scores 0 by construction. Drop the flag for a run that needs Δ. |
| `--runs` | default, 3 | One run of a non-deterministic agent says little. |
| `--max-cost-usd` | none | Runs are already bounded by each case's `max_turns` and `timeout_seconds`, and usage is felt as plan session limits rather than dollars; the reported cost is a list-price estimate only. |

A run of the four smoke cases is 12 agent runs; it took about 2.5 minutes at `-j 4` and reported $2.56. A run of the three lexicon fixture cases is 9 agent runs of about five minutes each; it took about 16 minutes at `-j 3` and reported $12.07.

## Cases

Each case is a directory with a `prompt.md` (frontmatter: run limits, tools, tags; body: the prompt) and `graders/*.md`. Runs start in an empty, sandboxed workspace with only the plugin loaded, no CLAUDE.md, memory or other plugins, so a prompt carries everything the task needs.

| Case | Checks |
|---|---|
| `smoke-design-interview` | `design-interview` fires on a pre-implementation pitch that doesn't name it |
| `smoke-design-philosophy` | `design-philosophy` fires on an implementation request whose structure is open |
| `smoke-adr` | `adr` fires when asked to write a decision up for the record |
| `smoke-lexicon` | `lexicon` fires when asked to review a glossary |
| `lexicon-shelfwise` | `lexicon` consolidates a 31-entry lexicon with planted defects (library lending, TypeScript) |
| `lexicon-stockroom` | the same on a 35-entry root `GLOSSARY.md` in another domain (warehouse, Python) |
| `lexicon-tessera` | the same on a smaller 22-entry lexicon (tiling window manager, C#). Held out: see below |
| `lexicon-tileand`, in `evals-tileand/` | the same on Tileand's real 63-entry lexicon, brought in at run time and graded against the owner's labels. Not part of an ordinary run: see below |

The smoke cases grade only `tool_used: Skill`, which can't pass without the plugin, so a baseline arm would tell them nothing beyond "the skill fired".

## Lexicon fixtures

`lexicon-shelfwise`, `lexicon-stockroom` and `lexicon-tessera` are invented projects whose lexicon is planted so the right answer is known by construction: each entry exercises one of the skill's rules, and the source code decides several verdicts in both directions, with things a correct run must find and decoys it must not fall for. They can be committed because nothing in them is real.

Each case directory holds:

- `fixture/`: the project, copied into the workspace by `scaffold.sh`. Nothing else is copied.
- `expected.md`: the verdict for every entry, the drift at `file:line`, the homeless sentence, the outside edges, the gap and the decoys; then what the graders check, what they leave ungraded and why.
- `graders/`: one deterministic `regex` grader per planted rule, on the written lexicon (entry headings kept or gone, a merge recorded, no entry over 80 words) and on the report (the drift and edge citations, the homeless sentence, the gap). One narrow `llm` grader per case, where a pattern can't decide.

The prompt gives sign-off in advance, since the skill waits for it before writing and a run has nobody to ask.

When writing a grader, keep three dashes in a row out of its frontmatter, comments and patterns included: the runner ends the frontmatter at the first one it meets, even mid-line, and the case then fails to load. In a pattern, write `-{3}`.

Shelfwise and Stockroom are regression fixtures: both were used while the skill's 0.5.0 text was tuned, and each `expected.md` says how. Items that flipped between those tuning runs are graded only where the key and its amendments leave one right answer.

## The Tileand case

`evals-tileand/lexicon-tileand` runs the consolidation on a real lexicon: Tileand's, as it stood at 63 entries before Tileand consolidated it. Tileand is where a weak skill shows first, so it is worth a case; it is not worth a copy. Tileand and this repository move at different paces, and a copy would go stale and invite fitting the skills to one project. So nothing of Tileand is kept here: the scaffold brings the lexicon, the decision records, the references and `src/` into the workspace at run time, from a pinned commit of your own checkout, with `git archive`, which only reads.

It lives in its own eval directory so that an ordinary run never sees it and the suite runs anywhere. To run it, write the path of a Tileand checkout into `evals-tileand/tileand-repo.path` (one line, gitignored), then:

```sh
claude plugin eval . --eval-dir evals-tileand --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold --allow-tools Write Edit
```

Results land in `evals-tileand/results/`, gitignored; `git status` is clean after a run. One run reads 199 files and takes about twelve minutes and 45 turns; three runs at `-j 3` took about 13 minutes and reported $13 to $14.

Two things about the runner decided that shape, neither of them in its documentation, both established by probe on Claude Code 2.1.278:

- **A scaffold script gets a scrubbed environment.** It sees `PATH`, a temporary `HOME` and a handful of others, and nothing else: no `EVAL_*` variable reaches it, whether exported in the shell or set in the case's `env:`. It can read outside the case directory, since it runs as you, outside the sandbox. Hence the pointer file, which the script finds through its own location.
- **A case cannot be skipped.** A scaffold script that exits non-zero makes the run an error: score 0, no turns, no cost, its message in the run's `error` field, and the suite exits 1. Without the pointer file this case fails that way, at once and for free, with a message saying what to create.

The graders are the owner's gold labels: `gone-*` and `kept-*` on the written lexicon's entry headings, one per labelled entry, and a few more for what a heading can't express. `expected.md` lists the verdicts and says which came from the owner and which were agreed by default. Both are generated by `gen-graders.py`, which lives with the labels outside this repository, along with the owner's reasons and a test that checks the graders against Tileand's own before and after. Regenerate them rather than editing them. Tileand's own consolidated lexicon fails exactly four graders, the four entries on which the owner disagrees with it.

This case is a regression input, like Shelfwise and Stockroom: iterate against it, but word any change to a skill as a general rule that holds for the other cases too, and read Tessera afterwards.

## Held out

Tessera is held out, so that there is always one input no iteration of the skill was tuned on. It was built by an agent that had seen neither the skill nor the other fixtures. It stays held out only under one rule: look at its score, but never edit the skill in response to a specific failure on it. Iterate on Shelfwise and Stockroom; read Tessera as the check that the iteration generalised. `--tag held-out` runs it alone. Once a Tessera failure has shaped the skill's wording, it is a regression fixture like the others and a new held-out one is needed.
