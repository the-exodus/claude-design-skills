# Working in the eval suite

`README.md` beside this file explains the suite. These are the rules that are costly to get wrong.

## Held-out cases: never fix a skill against them

`lexicon-tessera` and `lexicon-byre` are held out. **Look at their scores; never edit anything under `plugins/design/` in response to a specific failure on either.** They are the only evidence that a skill change generalised, and one edit made to fix a failure on them spends that for good.

- A defect that shows on a held-out case is worked on somewhere else: plant the same kind of trap in a regression fixture (`lexicon-shelfwise`, `lexicon-stockroom`), iterate there, word the change as a general rule, then read the held-out scores again.
- Fixing a grader, a rubric or an `expected.md` because it was wrong is allowed, on held-out cases too. The rule is about the skills' text.
- A new held-out fixture is built by a fresh agent that has seen neither the skill nor the other fixtures and keys, from a list of defect kinds only. Do not build one yourself after reading the skill.
- If asked to fix a skill and the evidence offered is a Tessera or Byre failure, say so before doing anything.

Every other case is a regression case and fair to iterate against.

## Before believing a result

- Read the failure in the run's trace (`evals/tools/show-turn.py`, with `--keep-temp`). Most failures in this suite's first runs were a grader that did not expect how a correct run had phrased something, not a defect in the run.
- Check each run's `error` in the `--json` result (`evals/tools/show-run.py`). A run that hit a usage limit scores 0 and the suite is not marked partial.
- Most of the skill defects here are intermittent. Judge a change over eight or more runs, never one.

## After changing something

- A skill that a resumed case loaded (any `history.jsonl`): `python3 evals/refresh-histories.py`, and commit the result. The transcript embeds the skill's text, and the case goes on testing the old wording otherwise.
- An `llm` grader's rubric: `python3 evals/tools/sync-calibration-rubrics.py`, then re-run that grader's calibration (`evals-calibration/`, about $0.30 to $0.70 a grading, so one grader at a time).
- A regex grader of a lexicon fixture: change the table in `evals/tools/lexicon-graders/gen-graders.mjs`, run `test-graders.mjs`, then `gen-graders.mjs write`.
- The Tileand case's graders and `expected.md` are generated from the owner's labels, which live outside this repository. Do not edit them by hand, and do not copy Tileand's lexicon, ADRs or source into this repository: naming its terms is fine, holding its content is not.

## Writing a grader or a case

- Three dashes in a row anywhere in a grader's frontmatter, comments and patterns included, end the frontmatter and stop the case loading. Write `-{3}` in a pattern.
- Quote a `description:` that contains a colon.
- `--case` is not repeatable and takes plain `*` wildcards; use one glob, or `--tag`.

## Running the suite from an agent session

Cases that write files need `--scaffold --allow-tools Write Edit`. In a worktree-isolated session the worktree guard refuses a shell command that contains the runner's subcommand name, reading it as shell `eval`: put the literal command in a small script file and run that. Do not disguise the command to get past a guard.
