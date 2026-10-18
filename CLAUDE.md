# claude-design-skills

Two plugins, each a directory the marketplace installs as it is: `design` (`plugins/design/skills/`) and `implementation` (`plugins/implementation/skills/`). `implementation` depends on `design`, never the reverse. The eval suite that checks them is under `evals/`, `evals-tileand/` and `evals-calibration/`.

## Before editing a skill because of an eval result

Four eval cases are held out:

| Held out | Guards | Regression fixtures to iterate on instead |
|---|---|---|
| `lexicon-tessera`, `lexicon-byre` | `plugins/design/` | `lexicon-shelfwise`, `lexicon-stockroom` |
| `review-heldout-quarry` | `plugins/implementation/` | the ferry cases: `lens-ferry`, `cycle-*` (fixture in `evals/review-fixtures/ferry/`) |
| `code-style-heldout-cinder` | `plugins/implementation/` | `code-style-lockerline`, and the Tileand case `code-style-tileand` |

**Never edit anything under the plugin a held-out case guards in response to a specific failure on it.** They are the only evidence that a skill change generalised rather than fitted the cases it was tuned against, and one edit made to fix a failure on them spends that for good.

If the evidence you were given for a skill change is a failure on a held-out case, say so before doing anything. The way to work on such a defect is to plant the same kind of trap in one of its regression fixtures, iterate there, word the change as a general rule, and read the held-out scores again afterwards. Every other case is fair to iterate against.

Read `evals/CLAUDE.md` before working with the evals or acting on their results: it has the rest, including what to run after changing a skill so that the resumed cases keep testing the current text.
