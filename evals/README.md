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
| `lexicon-byre` | the same on a 22-entry `docs/glossary.md` (dairy herd management, Go). Held out: see below |
| `lexicon-tileand`, in `evals-tileand/` | the same on Tileand's real 63-entry lexicon, brought in at run time and graded against the owner's labels. Not part of an ordinary run: see below |
| `adr-new-record` | `adr` numbers a new record after the highest, not into the gap; house format; the index gains its row |
| `adr-title-states-decision` | asked by topic, the title states what was decided |
| `adr-supersede-bold-status`, `-bare-status`, `-status-section` | the old record is marked in the status field it already has and is otherwise untouched; the new one names it; the index follows |
| `adr-partial-supersede-split` | one of two decisions changes: two successors, and the old record's status names both |
| `adr-no-directory` | with no ADR directory, it asks where, suggests a concrete place and creates nothing |
| `philosophy-before-implementation` | `design-philosophy` loads, by its qualified name, before the first edit of a request that adds behaviour |
| `philosophy-not-for-mechanical-edit`, `philosophy-not-for-rename` | it does not load for a typo fix or a rename |
| `philosophy-before-seeding` | in a design interview resumed at the scope confirmation, it loads before the tree is seeded |
| `philosophy-before-next-closure` | in an interview resumed after a branch closed without it, it loads before the next branch is worked |
| `interview-component-not-admitted` | a branch closes by introducing a module and a class: `design-interview` admits nothing to the lexicon |
| `interview-inherited-entry-unchanged` | a branch decides how an inherited concept is shown, not what it means: the inherited entry stays as it is |
| `interview-narrower-meaning-admitted` | a branch fixes what a word means: it is admitted, by meaning not mechanism, after `design:lexicon` is loaded |
| `interview-oversized-lexicon-noted` | a 34-entry lexicon is noted at ingestion and consolidation offered as separate work, not done |
| `interview-lexicon-write-back` | after the wrap-up, the lexicon is written back: inherited entries byte-identical, new terms as entries, and the reply says what is new and what changed |

The smoke cases grade only `tool_used: Skill`, which can't pass without the plugin, so a baseline arm would tell them nothing beyond "the skill fired".

## ADR cases

The `adr-*` cases run on Tidewatch, an invented project with a small ADR directory: records 0001, 0002 and 0004, so the gap at 0003 is there to be filled by mistake. Like the lexicon fixtures they copy a `fixture/` into the workspace and write files, so they need `--scaffold --allow-tools Write Edit`; `--tag adr` runs them alone. They are cheap: a run takes under a minute, and all seven at three runs each took about four minutes at `-j 4` and reported $5.86.

Nearly everything is graded from the files the run leaves behind. Where a case needs a known file name to read a new record back, the prompt gives the title to use; `adr-title-states-decision` leaves the title to the skill, and one narrow `llm` grader reads the created file's name. In the split case the successors' names are the run's to choose, so "supersedes part of" is matched in the session trace instead, on the old record's file name, which appears in none of the skill's references.

The supersede cases carry two graders on the new record: `new-names-what-it-supersedes`, that it has a `**Supersedes:**` link at all, and `supersedes-on-the-status-line`, that it sits on the status line after a middle dot, as `references/format.md` lays the header out. Under design 0.5.1, seven of eighteen runs put it on a line of its own, so these three cases fail about four times in ten until the skill changes; nothing else in the ADR cases failed once the graders were right.

The files are generated; the generator is not kept here. Edit them by hand.

## When design-philosophy loads

The `philosophy-*` cases check that `design-philosophy` loads when it should and only then. All are deterministic: `tool_used` on the `Skill` call, and a `regex` over the session trace for order, written so that one pattern covers a run that edits a file and a run that rewrites it whole. `--tag philosophy` runs the five; they need `--scaffold --allow-tools Write Edit`. Fifteen runs took under three minutes at `-j 4` and reported $3.83.

The failure these guard against is intermittent, so read them over several runs rather than one. Under design 0.5.1, over eight runs each: `philosophy-before-seeding` passed eight times, `philosophy-before-implementation` twice, `philosophy-before-next-closure` three times; the two "not for" cases never failed in three. Against the plugin as released at 0.5.0 the two that fail passed in none of five runs each, so they reproduce the original failure and 0.5.1 improved on it without fixing it. Where they fail, the skill is never called at all: an implementation request is carried out without it, and an interview whose tree already exists works the next branch without noticing the principles were never loaded.

### Resumed interviews and their transcripts

The two interview cases resume a conversation (`context.history_file` in `case.yaml`), and the case's prompt is the user's next turn. Established by probe on Claude Code 2.1.278, since the documentation says none of it: a history needs only `user` and `assistant` records chained by `uuid` and `parentUuid`; the trace of a resumed run holds only its new messages, so an order check sees exactly what happened after the resume; and a resumed run saves no session file in its kept run directory. Instead it writes the resumed session into the case directory, beside `history.jsonl`, in a file named by the history's session id, and appends to it on every run. Each run still starts from `history.jsonl` alone, so runs do not see one another; the file is gitignored so that `git status` stays clean after a run.

The transcripts are of an invented project and were produced by the runner itself: a run's stored session (under `config/projects/` in a kept run directory) was cut down to the conversation, and each later turn was appended from the next run's trace, with the user's replies written by hand. For `philosophy-before-next-closure` the tree had to be one really seeded without the principles. 0.5.0 loaded them when tried, the failure being intermittent, so that history was generated with `design-philosophy` removed from a copy of the 0.5.0 plugin, through a first branch closed under the interview's own four locks.

A transcript goes stale. When a skill loads, its whole body is written into the conversation, so a committed history freezes the text of every skill it loaded: edit `design-interview`, and these cases would go on testing the old wording. After editing a skill, run

```sh
python3 evals/refresh-histories.py          # rewrite the skill text embedded in every history
python3 evals/refresh-histories.py --check  # exit 1 if any history is stale
```

and commit the result. Only the embedded skill text changes; what the assistant said in the history stays as written, which is the point where a case starts from a failure state.

A skill called with arguments has them appended to its embedded text as an `ARGUMENTS:` block; the tool keeps that block as it is.

### Lexicon admission inside the interview

The `interview-*` cases cover the half of the lexicon rules that the consolidation fixtures never reach: `design-interview` admitting or refusing words at a branch closure, and leaving inherited entries alone. That is where sprawl starts. `--tag lexicon-admission` runs the five.

Four of them resume one invented interview, about a station that stops answering, on a project with a five-entry lexicon. The interview was chained turn by turn on design 0.5.1, the user's replies written by hand, and each case's history stops where the assistant has asked its probes; the case's prompt is the user's reply that closes the branch, so the run's one message is the closure. The fifth, the oversized lexicon, starts from the pitch on a fixture whose lexicon has 34 entries, a good many of them function and file names.

What a word's admission means is a judgement, so these cases use narrow `llm` graders, each asking one question of one short reply, beside the deterministic ones: no entry drafted for a component, no rewritten *stale* entry, `design:lexicon` loaded (`tool_used`), and for the write-back the file itself: the five inherited entries byte-identical, *miss* and *silent* present as entries, no component name and no mechanism in them.

Under design 0.5.1, over eight runs each unless said: the component was never admitted (three of three), the inherited entry never touched (eight of eight), the write-back correct (three of three). `interview-narrower-meaning-admitted` passed four times in eight, and failed the same way each time: the word was admitted, by meaning, but `design:lexicon` was never loaded, though the interview skill says to load it before the first admission. `interview-oversized-lexicon-noted` passed seven times in eight after one grader fix: a correct run had called the 34 entries "40-odd", which the pattern did not accept. Its one remaining failure, on the offer of consolidation, came from a run whose trace was not kept. Eight more runs with traces kept all made the offer, and all in the word "consolidation", which the first pattern accepted; so that failure was most likely a run that did not make the offer, about one in sixteen, not a wording the pattern missed. The pattern had been widened meanwhile to the other natural ways of making the offer, and stays so.

Two things about the runner found on the way: `--case` is not repeatable (the last one wins) and takes plain `*` wildcards only; and a `plugins:` entry may not point at a directory beside the cases, so a case that ships its own plugin copy keeps it in its own subdirectory.

## Lexicon fixtures

`lexicon-shelfwise`, `lexicon-stockroom`, `lexicon-tessera` and `lexicon-byre` are invented projects whose lexicon is planted so the right answer is known by construction: each entry exercises one of the skill's rules, and the source code decides several verdicts in both directions, with things a correct run must find and decoys it must not fall for. They can be committed because nothing in them is real.

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

This case is a regression input, like Shelfwise and Stockroom: iterate against it, but word any change to a skill as a general rule that holds for the other cases too, and read the held-out cases afterwards.

## Held out

Tessera and Byre are held out, so that there are always inputs no iteration of the skill was tuned on. Each was built by an agent that had seen neither the skill nor the other fixtures, from a list of defect kinds only. They stay held out under one rule: look at their scores, but never edit the skill in response to a specific failure on one. Iterate on Shelfwise, Stockroom and the Tileand case; read Tessera and Byre as the check that the iteration generalised. `--tag held-out` runs the two alone. Once a failure on one of them has shaped the skill's wording, that one is a regression fixture like the others and a new held-out one is needed.

There are two because they catch different things. Tessera is a tiling window manager, the same kind of system as Tileand, which the skill was first tuned on: it shares none of Tileand's text, so it catches fitting to Tileand's wording and structure, but it is weaker at catching fitting to that domain. Byre, dairy herd management, shares nothing with any other input here.

## Judge calibration

Every skill here produces judgement, so some grading is `llm`, and an uncalibrated judge gives a score that moves for reasons that have nothing to do with the skill. The suite keeps its `llm` graders narrow, one question each of one output, and `evals-calibration/` checks each of them against outputs whose right verdict is known.

A calibration case is a fixed output in `fixture/output.md`, named `<grader>--<pass|fail>-<n>` for the verdict it should get, with the grader's own rubric pointed at that file and an agent that has nothing to do, so only the judge is exercised. The known passes are real run outputs, read and judged by hand; the known fails are the same outputs with one paragraph changed: a sentence called homeless, a decoy given as its home, a component admitted under a friendlier name, a word defined by stored flags and a file path. The rubrics are copies: after changing a grader's rubric in `evals/`, run `python3 evals/tools/sync-calibration-rubrics.py` to copy it into that grader's calibration cases, and run them again.

```sh
claude plugin eval . --eval-dir evals-calibration --judge-model claude-opus-5 --ablation none --scaffold --runs 5 -j 8 --json calibration.json
python3 evals-calibration/score.py calibration.json
```

The command exits 1 by design, since every known fail "fails"; `score.py` is what says whether the judge is sound, and it exits 1 if any grader is below the bar. It reports, per grader, **agreement** (gradings that matched the known verdict), **flips** (fixed outputs that did not get the same verdict on every re-grade) and **split** (gradings on which the judge's three votes disagreed, a quieter sign of noise).

**The bar, provisional until the owner sets one:** agreement of at least 0.9 and no flips over five re-grades. A grader below it is reworded or replaced by a deterministic one.

Agreement reached with `claude-opus-5` as the judge, five gradings of each output, on 2026-09-20:

| Grader | Case | Outputs | Agreement | Flips | Split votes |
|---|---|---|---|---|---|
| `checkin-sentence-home` | `lexicon-shelfwise` | 5 | 25/25 | 0 | 0 |
| `cycle-count-distinction` | `lexicon-stockroom` | 5 | 25/25 | 0 | 0 |
| `single-window-sentence-home` | `lexicon-tessera` | 5 | 25/25 | 0 | 0 |
| `forty-day-sentence-home` | `lexicon-byre` | 5 | 25/25, after rewording; 24/25 with one flip before | 0 | 0 |
| `title-states-the-decision` | `adr-title-states-decision` | 5 | 25/25 | 0 | 0 |
| `component-not-admitted` | `interview-component-not-admitted` | 4 | 20/20 | 0 | 0 |
| `inherited-entry-unchanged` | `interview-inherited-entry-unchanged` | 4 | 20/20 | 0 | 0 |
| `term-admitted` | `interview-narrower-meaning-admitted` | 4 | 20/20 | 0 | 0 |
| `entry-states-meaning-not-mechanism` | `interview-narrower-meaning-admitted` | 5 | 25/25 | 0 | 0 |
| `does-not-consolidate` | `interview-oversized-lexicon-noted` | 4 | 20/20 | 0 | 0 |
| `says-what-is-new-and-what-changed` | `interview-lexicon-write-back` | 4 | 20/20 | 0 | 0 |

What calibration found was in the rubrics, not the judge. Writing down known verdicts for the three sentence-home graders showed that their rubric said both PASS and FAIL of a report that names the true home and the decoy together, which a real Tessera run had done and the judge had passed; and that it named a whole file as the decoy where only one doc comment is, which would have failed a real Byre run for citing the code that implements the behaviour. Then the first full run showed one grader flipping on a real output, because "at or around lines 49-50" left the judge to decide whether line 54 was around line 49. The rubrics now identify the decoy by quoting the comment. A rubric that can be read two ways is where a judge's noise comes from.

It is not cheap. A grading is three judge votes over the whole output, and judging a file reported about ten times the cost that judging a run's last message did in the ordinary suite: the full run of 250 gradings took three minutes and reported $70, and the two long-report graders alone $29. Calibrate one grader at a time with `--tag <grader>` after changing its rubric, and use `--runs 3` unless flips are what you are looking for.

Not covered yet: the owner's Tileand labels. The Tileand case has no `llm` graders, so there is nothing of it to calibrate; if narrow `llm` graders are added there for rewrites and reframes, the owner's one-line reasons in the private label file are the known verdicts to build their calibration outputs from.

## Tools

`evals/tools/` holds what was needed to build and debug this suite and will be needed again. All run from the repository root; each file's header says more.

| Tool | Use |
|---|---|
| `show-run.py result.json` | One line per run of a `--json` result, with the graders that failed and each run's `error`, which is where a usage-limit failure shows. |
| `show-turn.py <trace.jsonl>` | What a run did, in order, from a trace kept with `--keep-temp`: each tool call and each message. Read a failure here before believing it: most failures in this suite's first runs were a grader that did not expect how a correct run had phrased something. |
| `clean-kept-runs.py result.json` | Removes the run directories a finished pass kept, and only those. They hold directories sealed at mode 000, so plain `rm` fails, and a wildcard would hit runs still in progress. |
| `make-history.py`, `extend-history.py` | Build the transcript a resumed case needs (`context.history_file`) from the runner's own output: the first from a kept run's stored session, the second one exchange at a time from each resumed run's trace. They strip machine paths and refuse to write a history that still has one. Follow with `evals/refresh-histories.py`. |
| `sync-calibration-rubrics.py` | Copies each `llm` grader's rubric into its calibration cases; `--check` exits 1 if a copy differs, and it names any `llm` grader that has no calibration case. |
| `lexicon-graders/` | The regex graders of the four invented lexicon fixtures as one table (`gen-graders.mjs`), an offline test of every pattern against a hand-made correct output and the untouched fixture (`test-graders.mjs`, with `samples/`), and a check that the files on disk match the table (`check-files.mjs`). Change a pattern in the table, test it, then `gen-graders.mjs write`. The generator leaves existing `llm` graders alone: their rubrics are calibrated and edited by hand. |

Not kept: the one-off scripts that built the ADR, `philosophy-*`, `interview-*` and calibration cases. Those cases are plain files now; edit them by hand. The Tileand case's graders are generated from the owner's labels by a script that lives with the labels, outside this repository.
