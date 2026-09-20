# claude-design-skills

The `design` plugin's skills are under `plugins/design/skills/`; that directory is all the marketplace installs. The eval suite that checks them is under `evals/`, `evals-tileand/` and `evals-calibration/`.

## Before editing a skill because of an eval result

Two eval cases are held out: `lexicon-tessera` and `lexicon-byre`. **Never edit anything under `plugins/design/` in response to a specific failure on either.** They are the only evidence that a skill change generalised rather than fitted the cases it was tuned against, and one edit made to fix a failure on them spends that for good.

If the evidence you were given for a skill change is a Tessera or Byre failure, say so before doing anything. The way to work on such a defect is to plant the same kind of trap in a regression fixture (`lexicon-shelfwise`, `lexicon-stockroom`), iterate there, word the change as a general rule, and read the held-out scores again afterwards. Every other case is fair to iterate against.

Read `evals/CLAUDE.md` before working with the evals or acting on their results: it has the rest, including what to run after changing a skill so that the resumed cases keep testing the current text.
