# Evals

The design plugin's eval suite, run with Claude Code's own runner, [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). It lives at the repo root rather than inside `plugins/design/`, so it never ships with the plugin: the marketplace installs `./plugins/design` and nothing outside it.

## Run

From the repo root:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5
```

The repo root has no `plugin.json`; each case names the plugin under test itself, with `plugins: ["../../plugins/design"]` in its frontmatter. `--eval-dir` can't do this, since it only accepts a directory below the plugin.

Results land in `evals/results/<timestamp>/` (`aggregate-result.json`, `report.html`), which is gitignored. The command exits 0 when every case meets `--threshold` (default 1.0), 1 when one doesn't, 2 on a partial run.

To iterate on one case cheaply, run one arm once, then confirm at the default three runs before trusting the change:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --case <case-name> --runs 1 --ablation none
```

`--tag smoke` runs only the smoke cases; `-j 4` runs four agent runs at once against the same rate limit.

## Pinned settings

| Setting | Value | Why |
|---|---|---|
| `--model` | `claude-opus-5` | The skills are used from Opus sessions, and whether a skill triggers depends on the model, so the agent under test is the model they actually meet. Pinned so a model rollout isn't read as a plugin regression. |
| `--judge-model` | `claude-opus-5` | The default judge is a small fast model; the rubrics here ask for design judgement. |
| `--runs` | default, 3 per arm | One run of a non-deterministic agent says little. |
| `--max-cost-usd` | none | Runs are already bounded by each case's `max_turns` and `timeout_seconds`, and usage is felt as plan session limits rather than dollars; the reported cost is a list-price estimate only. |

A full two-arm run of the four smoke cases is 24 agent runs. With-arm only, it took about 2.5 minutes at `-j 4` and reported $2.56.

## Cases

Each case is a directory with a `prompt.md` (frontmatter: run limits, tools, tags; body: the prompt) and `graders/*.md`. Runs start in an empty, sandboxed workspace with only the plugin loaded, no CLAUDE.md, memory or other plugins, so a prompt carries everything the task needs.

| Case | Checks |
|---|---|
| `smoke-design-interview` | `design-interview` fires on a pre-implementation pitch that doesn't name it |
| `smoke-design-philosophy` | `design-philosophy` fires on an implementation request whose structure is open |
| `smoke-adr` | `adr` fires when asked to write a decision up for the record |
| `smoke-lexicon` | `lexicon` fires when asked to review a glossary |

The smoke cases grade only `tool_used: Skill`. Where that is a case's only grader it is scored in both arms, so the no-plugin arm scores 0 by construction and their Δ says nothing beyond "the skill fired".

## Fixtures

`context.add_dirs` and every other path in a case must name something inside the case directory. The runner rejects, when it loads the case, an absolute path, a path with `..`, and a symlink that resolves outside the case directory and the plugin (observed on Claude Code 2.1.278; the docs say "inside the case directory" but not how a link is treated). A fixture that must not be committed therefore either sits gitignored inside its case directory, or is created in the workspace by a `context.scaffold_script`, which runs as you, outside the sandbox, and only under `--scaffold`.
