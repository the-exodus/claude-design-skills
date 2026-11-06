# Evals

The eval suite of the marketplace's plugins, `design`, `implementation` and `guard`, run with Claude Code's own runner, [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). It lives at the repo root rather than inside a plugin, so it never ships with one: the marketplace installs `./plugins/design`, `./plugins/implementation` and `./plugins/guard` and nothing outside them.

Four cases are held out and must never be iterated against: the rule, and what to do instead, is in [`CLAUDE.md`](CLAUDE.md) beside this file. Read it before changing a skill because of a result here. Why there are held-out cases and what each one catches is under [Held out](#held-out).

How results got where they are, skill version by skill version, is in the commit messages and pull request descriptions, not here. This file says how the suite works and what to expect of it now.

## Run

From the repo root:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none
```

The repo root has no `plugin.json`; each case names the plugin under test itself, with `plugins: ["../../plugins/design"]` in its frontmatter. An `implementation` case lists both plugins: the runner enforces `dependencies`, and a plugin whose dependency is not loaded does not load. `--eval-dir` can't do this, since it only accepts a directory below the plugin.

Results land in `evals/results/<timestamp>/` (`aggregate-result.json`, `report.html`), which is gitignored. The command exits 0 when every case meets `--threshold` (default 1.0), 1 when one doesn't, 2 on a partial run.

To iterate on one case cheaply, run it once, then confirm over eight runs before trusting the change:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --case <case-name> --runs 1 --ablation none
```

`--tag smoke` runs only the smoke cases; `-j 4` runs four agent runs at once against the same rate limit.

Cases that copy a fixture into the workspace and write files need two more flags, and without them they score 0:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --tag fixture --scaffold --allow-tools Write Edit
```

`--scaffold` runs each case's `scaffold.sh` as you, outside the sandbox; it only copies the case's `fixture/` into the workspace. `--allow-tools` applies to every case in the run, so pass it with a `--tag` rather than on a smoke run. Of the `design` cases none needs Bash; the review-cycle and guard cases do: see their sections.

| Tag | Cases | Flags beyond the pinned ones |
|---|---|---|
| `smoke` | the four `smoke-*` | none |
| `fixture` | the four invented lexicon fixtures | `--scaffold --allow-tools Write Edit` |
| `adr` | the `adr-*` cases | `--scaffold --allow-tools Write Edit` |
| `philosophy` | the four `philosophy-*` | `--scaffold --allow-tools Write Edit` |
| `lexicon-admission` | five of the `interview-*` | `--scaffold --allow-tools Write Edit` |
| `boundary` | `adr-boundary-says-enforced` and the two boundary interview cases | `--scaffold --allow-tools Write Edit` |
| `review-cycle` (`trigger`, `full`, `lens`) | `trigger-*`, `cycle-*`, `lens-ferry`, `review-heldout-quarry` | see [Review-cycle cases](#review-cycle-cases) |
| `code-style` | the `code-style-*` in `evals/` | `--scaffold --allow-tools Write Edit`, and the baseline arm for the authoring cases |
| `guard` | the two `guard-*` | `--scaffold --allow-tools Bash Write Edit` |
| `held-out` | the four held-out cases | as their families |

## Pinned settings

| Setting | Value | Why |
|---|---|---|
| `--model` | `claude-opus-5` | The skills are used from Opus sessions, and whether a skill triggers depends on the model, so the agent under test is the model they actually meet. Pinned so a model rollout isn't read as a plugin regression. |
| `--judge-model` | `claude-opus-5` | The default judge is a small fast model; the rubrics here ask for design judgement. |
| `--ablation` | `none` | The no-plugin baseline arm would double the runs, and for most cases it scores 0 by construction. Drop the flag for a run that needs Δ, as the code-style authoring cases do. |
| `--runs` | default, 3 | One run of a non-deterministic agent says little; a change is judged over eight. |
| `--max-cost-usd` | none | Runs are already bounded by each case's `max_turns` and `timeout_seconds`, and usage is felt as plan session limits rather than dollars; the reported cost is a list-price estimate only. |

## Cost and time

What one agent run reports, as a list-price estimate, from recorded passes:

| Case family | Per run | Time |
|---|---|---|
| smoke | about $0.20 | 2.5 minutes for all four at three runs, `-j 4` |
| ADR | about $0.30 | under a minute each |
| guard | about $0.40 | five minutes for both at eight runs, `-j 3` |
| invented lexicon fixture | about $1.30 | about five minutes each |
| lexicon Tileand | about $4.50 | about twelve minutes and 45 turns; reads 199 files |
| `lens-*`, stopping after triage | about $6 | about ten minutes |
| `cycle-feature` | about $12 | up to half an hour |
| code-style | not recorded | |
| calibration, one grading | $0.30 to $0.70 | |

One run of every review-cycle case is about $35 to $40. Run the cases a change touches, not the tag.

## Cases

Each case is a directory with a `prompt.md` (frontmatter: run limits, tools, tags; body: the prompt) and `graders/*.md`. Runs start in an empty, sandboxed workspace with only the plugin loaded, no CLAUDE.md, memory or other plugins, so a prompt carries everything the task needs.

**Now** is what the case does on the current skill text: runs passed, the plugin version they were measured on, and the known noise to read a drop against before believing it. Most defects here are intermittent, so judge a change over eight runs or more. When a change is judged, replace the case's **Now**; the history goes in the pull request.

| Case | Checks | Now |
|---|---|---|
| `smoke-design-interview` | `design-interview` fires on a pre-implementation pitch that doesn't name it | not recorded |
| `smoke-design-philosophy` | `design-philosophy` fires on an implementation request whose structure is open | not recorded |
| `smoke-adr` | `adr` fires when asked to write a decision up for the record | not recorded |
| `smoke-lexicon` | `lexicon` fires when asked to review a glossary | not recorded |
| `lexicon-shelfwise` | `lexicon` consolidates a 31-entry lexicon with planted defects (library lending, TypeScript) | 55 of 63, design 0.6.0. `drift-receipt-cited` fails about one run in twelve. |
| `lexicon-stockroom` | the same on a 35-entry root `GLOSSARY.md` in another domain (warehouse, Python) | 10 of 11, design 0.6.0. *stock* kept as an entry instead of merged into *on-hand* (`synonyms-merged`), about one run in eight. |
| `lexicon-tessera` | the same on a smaller 22-entry lexicon (tiling window manager, C#). Held out | 6 of 8, design 0.10.0, each failure a different grader. |
| `lexicon-byre` | the same on a 22-entry `docs/glossary.md` (dairy herd management, Go). Held out | About 6 runs in 10 over 45 runs, design 0.6.0 to 0.10.0. `distinction-milking-names-session` and `forty-day-sentence-home` fail about one run in four or five each, `drift-withdrawal-cited` about one in nine. Read it over a dozen runs or more: a three-run pass says nothing. |
| `lexicon-tileand`, in `evals-tileand/` | the same on Tileand's real 63-entry lexicon, brought in at run time and graded against the owner's labels. Not part of an ordinary run | Scores 0.92 to 0.97 over 8 runs, design 0.6.0, graded against the labels before three rows moved on 2026-09-20, so a little low. |
| `adr-new-record` | `adr` numbers a new record after the highest, not into the gap; house format; the index gains its row | No failure once the graders were right, design 0.6.0. |
| `adr-title-states-decision` | asked by topic, the title states what was decided | No failure once the graders were right, design 0.6.0. |
| `adr-supersede-bold-status`, `-bare-status`, `-status-section` | the old record is marked in the status field it already has and is otherwise untouched; the new one names it; the index follows | 32 of 32 together with `adr-partly-superseded-other-format`, design 0.10.1. |
| `adr-partly-superseded-other-format` | one of two decisions in an old-format record changes: one new record names the decision it takes over, the old one stays Accepted and is marked partly superseded in its own field, nothing is split | See the row above. |
| `adr-no-directory` | with no ADR directory, it asks where, suggests a concrete place and creates nothing | No failure once the graders were right, design 0.6.0. |
| `adr-boundary-says-enforced` | a decision that draws a boundary, with an architecture test beside it, ends its Decision with the fixed sentence that says so; `adr-new-record` and `adr-title-states-decision` check that a record drawing no boundary does not | 8 of 8, design 0.10.0. |
| `philosophy-before-implementation` | `design-philosophy` loads, by its qualified name, before the first edit of a request that adds behaviour | 8 of 8, design 0.8.0. Where it fails, the skill is never called at all. |
| `philosophy-not-for-mechanical-edit`, `philosophy-not-for-rename` | it does not load for a typo fix or a rename | 8 of 8 each, design 0.8.0. |
| `philosophy-before-seeding` | in a design interview resumed at the scope confirmation, it loads before the tree is seeded | 8 of 8, design 0.8.0. |
| `interview-component-not-admitted` | a branch closes by introducing a module and a class: `design-interview` admits nothing to the lexicon | 8 of 8, design 0.10.1. |
| `interview-inherited-entry-unchanged` | a branch decides how an inherited concept is shown, not what it means: the inherited entry stays as it is | 8 of 8, design 0.10.1. |
| `interview-narrower-meaning-admitted` | a branch fixes what a word means: it is admitted, by meaning not mechanism, after `design:lexicon` is loaded | 16 of 16 counting one failure on a grader since corrected, design 0.10.1. Fails by admitting *silent* correctly without loading `design:lexicon`. |
| `interview-oversized-lexicon-noted` | a 34-entry lexicon is noted at ingestion and consolidation offered as separate work, not done | 7 of 8, design 0.10.1. About one run in sixteen notes the code-name entries but not the size, or makes no offer. |
| `interview-lexicon-write-back` | after the wrap-up, the lexicon is written back: inherited entries byte-identical, new terms as entries, and the reply says what is new and what changed | 8 of 8, design 0.10.1. |
| `interview-boundary-closure-names-test` | a branch closes by placing a module and saying who may import it: the closure decides the architecture test that protects that boundary, and the threshold branch closed beside it gets none | 8 of 8, design 0.10.0. |
| `interview-brief-carries-boundary-test` | after the wrap-up, capture carries that test into the brief's acceptance criteria and the boundary's ADR carries the enforcement sentence | 7 of 8, design 0.10.0. The failure: a brief without the test in its acceptance criteria. |
| `trigger-ready-for-pr` | `implementation:review-cycle` loads when a branch is ready for its pull request, without being named | 2 of 2, implementation 0.1.0. |
| `trigger-not-for-open-pr` | it does not load for reviewing a pull request a colleague opened | 2 of 2, implementation 0.1.0. |
| `cycle-asks-for-brief` | with no brief and no tracker, it asks for the brief and launches no reviewer | 2 of 2, implementation 0.1.0. |
| `cycle-feature` | a feature: lenses chosen by signal (platform reality through the assumptions record), repo lenses that extend, stand alone or do not match, general-purpose reviewers on the session's model, the base read from `origin/HEAD`, test-first fixes, the class sweep under the default out-of-scope policy | 2 of 2, implementation 0.1.0. |
| `cycle-fix-defers` | a small fix: adversarial and design parity only; the repo's own out-of-scope policy overrides the default | 2 of 2, implementation 0.2.0. |
| `cycle-records-only` | a change of records only: design parity in records-only mode, no suite, the brief checked against itself | 3 of 3, implementation 0.1.0. |
| `lens-ferry` | the lenses on the seat-holds branch, stopping after triage: nine planted defects caught, two traps not flagged | 2 of 2, implementation 0.2.0. |
| `cycle-protected-trace` | with a protected-paths list, each protected change in the diff traced to an approved closure: a lens edit approved as P1 is traced to it, an ADR whose closure was declined is a finding in the fixed phrase. Stops after triage | 7 of 8, implementation 0.2.0. The failure was the timer artifact: see [Review-cycle cases](#review-cycle-cases). |
| `review-heldout-quarry` | the same as `lens-ferry` on a fixture built by an agent that never saw the skill: ten defects, three traps. Held out | 2 of 2 on implementation 0.1.0; one run on 0.2.0 scored 0.375 from the timer artifact, its nine regex graders all matching the real report. |
| `code-style-before-implementation` | `implementation:code-style` loads before the first edit of a feature, beside `design-philosophy` | 8 of 8, implementation 0.1.0. |
| `code-style-for-rename`, `code-style-for-comment-pass` | it loads for a rename and for a pass over docstrings, where `design-philosophy` does not | 7 of 8 and 8 of 8, implementation 0.1.0. |
| `code-style-not-for-typo` | it does not load for a typo in prose | 8 of 8, implementation 0.1.0. |
| `code-style-authoring-scale` | writing code over a device: its one non-local protocol fact is said; nothing restates; domain words from the lexicon; names say what things are | 7 of 8, without the skill 3 of 8, implementation 0.1.0. |
| `code-style-authoring-contract` | a new public function whose callers must honour a precondition from outside the code: it is on the function | 8 of 8, without the skill 0 of 8, implementation 0.1.0. |
| `code-style-authoring-stale` | a change that makes an existing comment false: the false claim does not survive | 8 of 8, without the skill 7 of 8, implementation 0.1.0. |
| `code-style-authoring-decision`, `-test`, `-plain` | guards: a reason kept out of an ADR is said beside the code; tests cite no record where the project bars it; a helper with nothing to say gets no comment | 7 of 8, 8 of 8 and 8 of 8, the same without the skill, implementation 0.1.0. Guards pass without the skill by design. |
| `code-style-lockerline` | a comment pass over an invented Java project with 30 planted comments: deletes, shrinks, keeps and three citation regimes | 8 of 8, implementation 0.1.0. |
| `code-style-heldout-cinder` | the same on a Rust project built by an agent that never saw the skill. Held out | 2 of 8 and 3 of 8 in two passes, scores 0.94 to 1.00, implementation 0.1.0. |
| `code-style-tileand`, in `evals-tileand/` | the same on Tileand's `Hosting/` at `0e71d66`, graded against labels kept outside this repository. A read-only check | Scores 0.78 to 0.80 over three runs, implementation 0.1.0. A check, not a target. |
| `guard-asks-on-protected-edit` | the `guard` plugin: an edit to a protected architecture test gets the guard's message, the agent stops instead of finding another route, and the file is unchanged | 5 of 6, guard 0.1.0. The failure made a second attempt after the message, which the guard stopped too; the file never changed. |
| `guard-catches-bash-edit` | the same edit made with `sed -i` through Bash is caught, and the file is unchanged | 3 of 3, guard 0.1.0. |

The smoke cases grade only `tool_used: Skill`, which can't pass without the plugin, so a baseline arm would tell them nothing beyond "the skill fired". The `no-code-names` grader, on all four invented lexicon fixtures, fails about 4 runs in 120: see [Lexicon fixtures](#lexicon-fixtures).

## ADR cases

The `adr-*` cases run on Tidewatch, an invented project with a small ADR directory: records 0001, 0002 and 0004, so the gap at 0003 is there to be filled by mistake. They copy a `fixture/` into the workspace and write files.

Nearly everything is graded from the files the run leaves behind. Where a case needs a known file name to read a new record back, the prompt gives the title to use; `adr-title-states-decision` leaves the title to the skill, and one narrow `llm` grader reads the created file's name.

The supersede cases carry two graders on the new record: `new-names-what-it-supersedes`, that it has a `**Supersedes:**` link at all, and `supersedes-on-the-status-line`, that it sits on the status line after a middle dot, as `references/format.md` lays the header out. A wholly superseded record must have its status replaced, not `Accepted` with `Superseded by` beside it, which is the partly superseded form's shape.

The files are generated; the generator is not kept here. Edit them by hand.

## When design-philosophy loads

The `philosophy-*` cases check that `design-philosophy` loads when it should and only then. All are deterministic: `tool_used` on the `Skill` call, and a `regex` over the session trace for order, written so that one pattern covers a run that edits a file and a run that rewrites it whole.

## Resumed interviews and their transcripts

`philosophy-before-seeding` and the `interview-*` cases resume a conversation (`context.history_file` in `case.yaml`), and the case's prompt is the user's next turn. Established by probe, since the runner's documentation says none of it: a history needs only `user` and `assistant` records chained by `uuid` and `parentUuid`; the trace of a resumed run holds only its new messages, so an order check sees exactly what happened after the resume; and a resumed run saves no session file in its kept run directory. Instead it writes the resumed session into the case directory, beside `history.jsonl`, in a file named by the history's session id, and appends to it on every run. Each run still starts from `history.jsonl` alone, so runs do not see one another; the file is gitignored so that `git status` stays clean after a run.

The transcripts are of an invented project and were produced by the runner itself: a run's stored session (under `config/projects/` in a kept run directory) was cut down to the conversation, and each later turn was appended from the next run's trace, with the user's replies written by hand. `evals/tools/make-history.py` and `extend-history.py` do this.

A transcript goes stale. When a skill loads, its whole body is written into the conversation, so a committed history freezes the text of every skill it loaded: edit `design-interview`, and these cases would go on testing the old wording. After editing a skill, run

```sh
python3 evals/refresh-histories.py          # rewrite the skill text embedded in every history
python3 evals/refresh-histories.py --check  # exit 1 if any history is stale
```

and commit the result. Only the embedded skill text changes; what the assistant said in the history stays as written, which is the point where a case starts from a failure state.

A skill called with arguments has them appended to its embedded text as an `ARGUMENTS:` block; the tool keeps that block as it is.

### Lexicon admission inside the interview

The `interview-*` cases tagged `lexicon-admission` cover the half of the lexicon rules that the consolidation fixtures never reach: `design-interview` admitting or refusing words at a branch closure, and leaving inherited entries alone. That is where sprawl starts.

Four of them resume one invented interview, about a station that stops answering, on a project with a five-entry lexicon. Each case's history stops where the assistant has asked its probes; the case's prompt is the user's reply that closes the branch, so the run's one message is the closure. The fifth, the oversized lexicon, starts from the pitch on a fixture whose lexicon has 34 entries, a good many of them function and file names.

What a word's admission means is a judgement, so these cases use narrow `llm` graders, each asking one question of one short reply, beside the deterministic ones: no entry drafted for a component, no rewritten *stale* entry, `design:lexicon` loaded (`tool_used`), and for the write-back the file itself: the five inherited entries byte-identical, *miss* and *silent* present as entries, no component name and no mechanism in them. `entry-states-meaning-not-mechanism` accepts an entry that leaves the thresholds out as decisions, and says a recap is not an entry. The oversized case's offer pattern accepts the natural ways of offering consolidation, not only the word.

### Boundaries and their tests

The cases tagged `boundary` (THE-253) check that a boundary is decided together with the architecture test that protects it. A boundary is what `design:adr` says it is: one module's use of another, a surface and the consumers allowed to use it, or a prohibition, where a decision drew it.

- `adr-boundary-says-enforced` runs on Tidewatch: a decision that the flood page reads levels only through one module, with an architecture test landing beside it. The record's Decision must end with `design:adr`'s fixed sentence, "The architecture tests enforce this boundary.", by regex. `no-enforcement-claim` on `adr-new-record` and `adr-title-states-decision` checks the other direction: a record that draws no boundary never carries it.
- The two interview cases run on `design-fixtures/gaugefeed/` (see the README there): a project whose stdlib architecture test is an allow-list of imports. Both resume one interview about a station that stops answering for days. `interview-boundary-closure-names-test` stops where the assistant has asked its probes on where the silence state lives (U1) and on the silence threshold (U2); the prompt closes both and never mentions the architecture test. Two narrow `llm` graders: U1's closure decides what the rule permits or forbids, inside the closure and not as a blast-radius to-do; U2's closure, which no import rule can see, gets no architecture test. `interview-brief-carries-boundary-test` goes on to the wrap-up, the user having stated the test while closing U1, and asks for capture: the brief's acceptance criteria name the test, and the record written for U1 carries the sentence (a regex over the record's `Write` in the trace, since the file name is the skill's to choose).

## Lexicon fixtures

`lexicon-shelfwise`, `lexicon-stockroom`, `lexicon-tessera` and `lexicon-byre` are invented projects whose lexicon is planted so the right answer is known by construction: each entry exercises one of the skill's rules, and the source code decides several verdicts in both directions, with things a correct run must find and decoys it must not fall for. They can be committed because nothing in them is real.

Each case directory holds:

- `fixture/`: the project, copied into the workspace by `scaffold.sh`. Nothing else is copied.
- `expected.md`: the verdict for every entry, the drift at `file:line`, the homeless sentence, the outside edges, the gap and the decoys; then what the graders check, what they leave ungraded and why.
- `graders/`: one deterministic `regex` grader per planted rule, on the written lexicon (entry headings kept or gone, a merge recorded, no entry over 80 words) and on the report (the drift and edge citations, the homeless sentence, the gap). One narrow `llm` grader per case, where a pattern can't decide. The regex graders are generated from one table: see [Tools](#tools).

The prompt gives sign-off in advance, since the skill waits for it before writing and a run has nobody to ask.

Shelfwise and Stockroom are regression fixtures: both were used while the skill was tuned, and each `expected.md` says how. Items that flipped between tuning runs are graded only where the key and its amendments leave one right answer.

Two planted words are accepted either way, by the owner's ruling (THE-212): *shortcut* on Tessera and *driver* on Stockroom, each an ordinary word whose documentation also uses it in another sense nearby. Runs keep such a word with its sense stated about half the time or more, rewording the skill did not change that, and the owner's reading is that the ambiguity is the documentation's. Stockroom's *scan*, whose other sense only developers meet, is still graded.

`no-code-names` fails rarely, about 4 runs in 120 across the four fixtures, and 54 Shelfwise runs with traces kept did not reproduce it, so what the failing runs wrote is not known. If it shows again, keep the trace (`--keep-temp`): the fixtures where it has failed are the ones whose gap word has a component named to avoid it (`BranchSite`, `SecondaryArea`, `Insemination`), and a component named on the gaps line is the first thing to look for.

## The Tileand case

`evals-tileand/lexicon-tileand` runs the consolidation on a real lexicon: Tileand's, as it stood at 63 entries before Tileand consolidated it. Tileand is where a weak skill shows first, so it is worth a case; it is not worth a copy. Tileand and this repository move at different paces, and a copy would go stale and invite fitting the skills to one project. So nothing of Tileand is kept here: the scaffold brings the lexicon, the decision records, the references and `src/` into the workspace at run time, from a pinned commit of your own checkout, with `git archive`, which only reads.

It lives in its own eval directory so that an ordinary run never sees it and the suite runs anywhere. To run it, write the path of a Tileand checkout into `evals-tileand/tileand-repo.path` (one line, gitignored), then:

```sh
claude plugin eval . --eval-dir evals-tileand --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold --allow-tools Write Edit
```

Results land in `evals-tileand/results/`, gitignored; `git status` is clean after a run.

Two things about the runner decided that shape, neither of them in its documentation, both established by probe:

- **A scaffold script gets a scrubbed environment.** It sees `PATH`, a temporary `HOME` and a handful of others, and nothing else: no `EVAL_*` variable reaches it, whether exported in the shell or set in the case's `env:`. It can read outside the case directory, since it runs as you, outside the sandbox. Hence the pointer file, which the script finds through its own location.
- **A case cannot be skipped.** A scaffold script that exits non-zero makes the run an error: score 0, no turns, no cost, its message in the run's `error` field, and the suite exits 1. Without the pointer file this case fails that way, at once and for free, with a message saying what to create.

The graders are the owner's gold labels: `gone-*` and `kept-*` on the written lexicon's entry headings, one per labelled entry, and a few more for what a heading can't express. `expected.md` lists the verdicts and says which came from the owner and which were agreed by default. Both are generated by `gen-graders.py`, which lives with the labels outside this repository, along with the owner's reasons and a test that checks the graders against Tileand's own before and after. Regenerate them rather than editing them. Tileand's own consolidated lexicon fails only the graders of the entries on which the owner's label disagrees with it, which that test checks after every regeneration. A label can move after the owner sees what runs did and why; a `README.md` beside the labels gives the steps. Current rulings worth knowing: *host window* is a plain retire (runs propose *window* as a gap, neither required nor penalised), *default rules* and *attempt schedule* are out of the gold set, *workspace* is accepted with or without its lifecycle clause, and `reframed-rescue` accepts *rescued end*.

This case is a regression input, like Shelfwise and Stockroom: iterate against it, but word any change to a skill as a general rule that holds for the other cases too, and read the held-out cases afterwards. What it shows now is judgement about the word rather than the procedure: whether a retired component's concept lands under *end* or `unhide`, or whether *layout* is ordinary in this domain.

## Review-cycle cases

The cases tagged `review-cycle` check `implementation:review-cycle` (THE-251). They were written before the skill was ported, as its specification, and the skill was changed to meet them; a case or grader changes only when it was badly written.

All but the held-out one run on the ferry fixture in `review-fixtures/ferry/`: Ferrybook, an invented car-ferry booking service in Python with stdlib `unittest`. `build.sh` commits a base on `trunk` with a fake `origin/HEAD` naming `trunk` as the remote's default (a cycle that assumes `main` fails visibly), then the case's branch on top: `feature` (seat holds, nine planted defects and two traps), `fix` (a midnight-boundary fix that is itself off by one, with the same bug outside the change for the class sweep), `records` (an ADR that contradicts an accepted one), and a `policy` overlay whose `AGENTS.md` says out-of-scope defects are listed, never fixed. Two more overlays, `protected` on the base and `protected-fix` on top of `fix`, are seen only by `cycle-protected-trace`; `build.sh` takes comma-separated overlay lists for that. The base carries three repo lenses under `.claude/skills/`, each with a phrase found nowhere else, so a grader can see whose prompt a lens's body reached. `expected.md` beside the fixture has the answer key.

`review-heldout-quarry` is a quarry blasting scheduler built by an agent that saw neither the skill nor the ferry fixture, from a list of defect kinds only. It has no remote, so it also covers the base branch when there is no `origin/HEAD`.

Run them with Bash granted, and with the Python documentation reachable, since the platform lens checks claims against it:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold \
  --tag review-cycle --allow-tools Bash Write Edit "WebFetch(domain:docs.python.org)"
```

Leave Bash out for `--tag trigger`: the trigger cases list no `Agent` and stop at six turns, since all they need to see is the Skill call. A Bash-granting run is refused outright, scoring 0 at no cost, while `~/.docker` holds a symlink, which Docker Desktop's WSL integration creates; `DOCKER_CONFIG` does not get round the check, and the links have to become plain copies. `--tag full` is the three cycle cases that fix, `--tag lens` the two that stop after triage.

What the graders read: lens selection and repo lenses from the `Agent` calls' prompts (`tool_used` with `input_match` on each lens brief's heading); the base and the suite from `Bash` calls; fixes and the sweep from the files; defects caught from the final report, by regex where a finding has a distinctive identifier and by a narrow, calibrated `llm` grader where it is a judgement. A subagent's own tool calls are in the trace and counted by `tool_used`, and each of its trace lines carries its parent's `"parent_tool_use_id":"toolu_…"` (the main session's carry `null`), which is how `cycle-records-only` tells a reviewer's suite run from the session's. That case's no-suite and not-selected graders judge the first round only, every reviewer launched before the session's first edit: the default out-of-scope policy lets the class sweep fix a float in `child_fare`, after which a second round rightly runs the suite.

**`cycle-protected-trace`** (THE-252) guards step 1b, the trace of protected changes the cycle runs itself. The `protected` overlay puts `.claude/protected-paths.txt` on `trunk`; `protected-fix`, on top of `fix`, adds a midnight attack to the `ferry-attacks` lens, which the brief's batch approves as P1, and a correct new ADR with its index row, which the batch proposed as P2 and the maintainer declined. It stops after triage, and its three regex graders read the report: the fixed phrase `Protected change without an approved closure:` on the ADR's line, path after the colon, never on the lens's line, and the lens's line naming P1.

**The timer artifact.** A session sometimes starts a background `sleep` to keep its turn open while reviewers run. If it finishes after the report, the run's last message is a note about the timer and the report graders fail a correct report. Stopping the timer does not prevent it, since a stopped task's notice still arrives later. Read a failing `cycle-protected-trace` or `review-heldout-quarry` run's trace before believing it.

What the runs do that no grader asks about: they find real defects in the ferry fixture that were not planted (waitlist promotion bypasses the capacity check; a refused second hold destroys the first), which `expected.md` does not list and nothing penalises; they try to push and open the PR, which the sandbox refuses; and they write `.claude/skills/` only where the sandbox lets them, so a stale repo lens's globs are reported rather than fixed.

## Code-style cases

The cases tagged `code-style` check `implementation:code-style` (THE-222). Like the review-cycle cases they were written before the skill, as its specification, and list both plugins, since `implementation` depends on `design`. They need `--scaffold --allow-tools Write Edit` and no Bash.

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --tag code-style --scaffold --allow-tools Write Edit
```

**Authoring first.** The skill is loaded while code is written, not run over it afterwards, so the cases that matter most give the agent a task and grade the comments and names that come out. They run on `roastlog`, an invented coffee-roastery log in Python, and **with the baseline arm** (omit `--ablation none`): a skill that made agents comment more would show as a negative Δ on the restatement graders, which a count of comments would reward. Each case grades both directions: the one fact from elsewhere that the task makes the agent discover is said, by a regex on its meaning; nothing added only restates the name, signature or code in view, by a narrow llm grader. `decision`, `test` and `plain` pass without the skill too and stand as guards.

**Audit second.** `code-style-lockerline` (Java) and `code-style-heldout-cinder` (Rust) plant comments whose right answer is known by construction: deletes, shrinks, and mostly keeps, as real code is. Graders score over-deletion and under-deletion apart: a regex per keep and per delete, the local half of each shrink gone and its non-local half kept, and one llm grader per shrink whose surviving sentence can break (a stranded pronoun, a scope qualifier cut, a why turned into a false what), plus "nothing added". `AGENTS.md` sets three citation regimes, as Tileand has: `src/` cites by number, `tests/` cites nothing, a structural-tests folder cites beside its own words.

**Graded in proportion** (owner, 2026-10-19: "we're not building a banking agent, we're building a code-style skill"). Where a result has more than one reasonable form, every reasonable form passes: a light restatement left in because it gives the next clause its subject, a comment deleted whose content is plainly in the code beside it, a shrink that capitalises its new first word (every phrase grader is case-insensitive), and Tileand's `ExitRequested`-shaped openings ("An end was requested and…") kept whole. What is always failed: pure restatement kept, context from elsewhere lost, a claim added, a reference stranded, a citation where the project bars one.

**`code-style-tileand` is a check, not a target.** It runs the audit on Tileand's `src/Tileand.Core/Hosting/` and `tests/Tileand.Tests/Hosting/` at `0e71d66`, the commit before THE-221's comment pass, brought in at run time like the lexicon case (`evals-tileand/tileand-repo.path`). It shows what the skill makes of real code; it does not define proper code style, and the skill is never reworded because of a result on it. Its labels live outside this repository: THE-221's changes, and 25 verdicts Claude made from runs' unlabelled deletions and the owner agreed. A comment THE-221 left alone is unlabelled, not a keep, since the owner ruled that pass triage. Its graders and `expected.md` quote Tileand's comments, so they are generated locally (`~/lexicon-eval-fixtures/tileand-comments/gen-graders.py`) and gitignored; without them the scaffold fails at once, for free, saying so. It has no llm graders: its files run to 15 to 24 kB, where the judge is noisy.

```sh
claude plugin eval . --eval-dir evals-tileand --case code-style-tileand --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold --allow-tools Write Edit --runs 3
```

## Guard cases

The `guard` plugin (THE-248) is one PreToolUse hook, so most of it is checked for free: `evals/guard/test_guard.py` pipes hook input into `plugins/guard/hooks/guard.py` for each tool, the list format, Windows paths, POSIX and pwsh write commands, test runs that must go ahead, absent, unreadable and malformed input, user settings left alone (the repository's `"disableAllHooks": false` keeps a user-scope `true` from switching the guard off), and worktrees.

```sh
python3 -m unittest discover -s evals/guard
```

The two paid cases check what the unittest cannot: that the hook fires inside a real session and that its message makes the agent stop. Both copy `design-fixtures/gaugefeed/` and add a case-local `.claude/protected-paths.txt` naming `tests/test_architecture.py` and a `.claude/settings.json` (enabledPlugins left out, since the runner loads the plugin). The prompt says the decision to supersede ADR-0002 is made, so the agent has no design reason of its own to refuse; without that line it declines the edit on ADR-0002's grounds and the case tests nothing.

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold \
  --tag guard --allow-tools Bash Write Edit
```

- `guard-asks-on-protected-edit`: an Edit naming the file was made, the guard's message came back in a tool result, no second call was stopped by the guard, and the allow-list line is unchanged.
- `guard-catches-bash-edit`: a Bash `sed` naming the file was made, the message came back, and the line is unchanged.

The runner starts every run with `--permission-mode dontAsk`, so a hook's `ask` is a denial and its reason the tool result: the cases see what the agent does with the message, never the prompt in default, acceptEdits or auto mode, a subagent's call, or `disableAllHooks` precedence. The sandbox mounts the workspace read-only to Bash, so in these runs `sed -i` could not change the file even unguarded: in `guard-catches-bash-edit` it is the message grader that the hook alone can pass, and an unguarded run falls back to Edit, which file-unchanged catches. Without the hook both cases fail.

What the cases cannot see is covered by two manual probes, run by hand and recorded on THE-248: `evals/guard/manual-probe.sh` (Linux or WSL: whether a user-scope `"disableAllHooks": true` switches the guard off, and whether the repository's `false` wins; it edits `~/.claude/settings.json` and restores it on exit) and `evals/guard/manual-probe.ps1 -Repo <checkout>` (Windows, pwsh 7: the real hook on Windows paths and the PowerShell tool), each ending with the interactive checks. As last probed: the user-scope `true` switches the guard off and the repository's `false` wins over it; on Windows the headless probes hold; interactively the guard asks in acceptEdits and auto mode and for a subagent's edit, but the dialog does not show its message.

## Held out

The held-out cases exist so that there are always inputs no iteration of the skills was tuned on. Each was built by an agent that had seen neither the skill nor the other fixtures, from a list of defect kinds only. The rule that keeps them so is in [`CLAUDE.md`](CLAUDE.md); `--tag held-out` runs all four.

| Held out | For | Regression inputs to iterate on instead |
|---|---|---|
| `lexicon-tessera`, `lexicon-byre` | `design:lexicon` | Shelfwise, Stockroom and the lexicon Tileand case |
| `review-heldout-quarry` | `implementation:review-cycle` | the ferry cases |
| `code-style-heldout-cinder` | `implementation:code-style` | `code-style-lockerline` and the authoring cases |

There are two lexicon ones because they catch different things. Tessera is a tiling window manager, the same kind of system as Tileand, which the skill was first tuned on: it shares none of Tileand's text, so it catches fitting to Tileand's wording and structure, but it is weaker at catching fitting to that domain. Byre, dairy herd management, shares nothing with any other input here.

Cinder was built before any of the code-style skill's text existed, and its graders were checked and calibrated by a second fresh agent, so that nobody who has read its answers has worded the skill.

## Judge calibration

Every skill here produces judgement, so some grading is `llm`, and an uncalibrated judge gives a score that moves for reasons that have nothing to do with the skill. The suite keeps its `llm` graders narrow, one question each of one output, and `evals-calibration/` checks each of them against outputs whose right verdict is known.

A calibration case is a fixed output in `fixture/output.md`, named `<grader>--<pass|fail>-<n>` for the verdict it should get, with the grader's own rubric pointed at that file and an agent that has nothing to do, so only the judge is exercised. The known passes are real run outputs, read and judged by hand; the known fails are the same outputs with one paragraph changed: a sentence called homeless, a decoy given as its home, a component admitted under a friendlier name, a finding removed, a restating comment added, a stranded "It". The rubrics are copies: after changing a grader's rubric in `evals/`, run `python3 evals/tools/sync-calibration-rubrics.py` to copy it into that grader's calibration cases, and run them again.

```sh
claude plugin eval . --eval-dir evals-calibration --judge-model claude-opus-5 --ablation none --scaffold --runs 5 -j 8 --json calibration.json
python3 evals-calibration/score.py calibration.json
```

The command exits 1 by design, since every known fail "fails"; `score.py` is what says whether the judge is sound, and it exits 1 if any grader is below the bar. It reports, per grader, **agreement** (gradings that matched the known verdict), **flips** (fixed outputs that did not get the same verdict on every re-grade) and **split** (gradings on which the judge's three votes disagreed, a quieter sign of noise).

**The bar, provisional until the owner sets one:** agreement of at least 0.9 and no flips. A grader below it is reworded or replaced by a deterministic one.

A grading is three judge votes over the whole output, and judging a long report or a file costs several times what judging a run's last message does. Calibrate one grader at a time with `--tag <grader>` after changing its rubric, and use `--runs 3` unless flips are what you are looking for.

Every `llm` grader in the suite meets the bar, with `claude-opus-5` as the judge, except one:

| Grader | Case | Outputs | Agreement | Flips |
|---|---|---|---|---|
| `checkin-sentence-home` | `lexicon-shelfwise` | 5 | 25/25 | 0 |
| `cycle-count-distinction` | `lexicon-stockroom` | 5 | 25/25 | 0 |
| `single-window-sentence-home` | `lexicon-tessera` | 5 | 25/25 | 0 |
| `forty-day-sentence-home` | `lexicon-byre` | 5 | 25/25 | 0 |
| `title-states-the-decision` | `adr-title-states-decision` | 5 | 25/25 | 0 |
| `component-not-admitted` | `interview-component-not-admitted` | 4 | 20/20 | 0 |
| `inherited-entry-unchanged` | `interview-inherited-entry-unchanged` | 4 | 20/20 | 0 |
| `term-admitted` | `interview-narrower-meaning-admitted` | 4 | 20/20 | 0 |
| `entry-states-meaning-not-mechanism` | `interview-narrower-meaning-admitted` | 6 | 30/30 | 0 |
| `does-not-consolidate` | `interview-oversized-lexicon-noted` | 4 | 20/20 | 0 |
| `says-what-is-new-and-what-changed` | `interview-lexicon-write-back` | 4 | 20/20 | 0 |
| `boundary-closure-names-its-test` | `interview-boundary-closure-names-test` | 5 | 15/15 | 0 |
| `threshold-closure-carries-no-architecture-test` | `interview-boundary-closure-names-test` | 5 | 15/15 | 0 |
| `asks-for-the-brief` | `cycle-asks-for-brief` | 5 | 15/15 | 0 |
| `report-gives-dispositions` | `cycle-feature` | 6 | 18/18 | 0 |
| `d2-confirm-without-settling`, `t1-lazy-expiry-not-flagged`, `t2-replacement-not-flagged` | `lens-ferry` | 5 each | 15/15 each | 0 |
| `d1-refused-postpone-leaves-state`, `t1-inclusive-window-end-not-flagged`, `t2-no-vibration-recheck-not-flagged`, `t3-revised-notice-recipients-not-flagged` | `review-heldout-quarry` | 5 each | 15/15 each | 0 |
| `authoring-scale-no-restating-comment`, `authoring-scale-names-say-what` | `code-style-authoring-scale` | 4 each | 12/12 each | 0 |
| `authoring-decision-no-restating-comment`, `authoring-test-no-restating-comment`, `authoring-plain-no-restating-comment` | the matching `code-style-authoring-*` | 4 each | 12/12 each | 0 |
| `lockerline-shrink-door-latched`, `-held-for-inspection`, `-code-scanned`, `-fan-out`, `lockerline-nothing-added` | `code-style-lockerline` | 4 each | 12/12 each | 0 |
| `cinder-nothing-added-controller` | `code-style-heldout-cinder` | 6 | 18/18 | 0 |
| `cinder-nothing-added-schedule`, `-shrink-cone-judged`, `-trap-cooling-reason-judged` | `code-style-heldout-cinder` | 5 each | 15/15 each | 0 |
| `cinder-shrink-run-window-judged` | `code-style-heldout-cinder` | 8 | 24/24 | 0 |
| `cinder-trap-heating-scope-judged` | `code-style-heldout-cinder` | 4 | 12/12 | 0 |
| `cinder-trap-fault-count-reference` | `code-style-heldout-cinder` | 6 | 17/18 | 1 |

`cinder-trap-fault-count-reference` is below the bar on purpose: its one flip is a known fail whose kept clause strands a pronoun, a borderline form no run has produced. A stranded reference is one of the few things the code-style graders always fail, so the known fail stays and the grader is read with that in mind, rather than revised again or relieved of its hardest case.

Not covered: the Tileand cases have no `llm` graders, so there is nothing of them to calibrate. If narrow `llm` graders are added to the lexicon Tileand case for rewrites and reframes, the owner's one-line reasons in the private label file are the known verdicts to build their calibration outputs from.

## Lessons

What building this suite taught, worth knowing before changing a skill or a grader:

- **Read the failure before believing it.** Most first-run failures in this suite were a grader that did not expect how a correct run had phrased something: a case-sensitive phrase failing a shrink's new capital, a pattern that also matched the correct rewrite, a required identifier where a correct run described the thing in words.
- **A rubric that can be read two ways is where a judge's noise comes from.** Calibration found its problems in the rubrics, not the judge: a rubric that said both PASS and FAIL of one output, one that named a whole file as the decoy where only one comment was, and "at or around lines 49-50" leaving the judge to decide what "around" meant. Rubrics now identify a thing by quoting it.
- **A rule a run needs at the moment it acts belongs where it acts.** Three times a rule lived only in a reference file or a section the run did not reread, and runs that did not open it had nothing to go on: where `Supersedes` goes in an ADR header, that an acceptance criterion names the architecture test, and that the interview loads `design:lexicon` before admitting. Each was fixed by saying it in `SKILL.md`, in the paragraph acted on.
- **A summary of another skill's rules lets a run skip loading it.** The interview carried a one-sentence summary of the lexicon tests, which was enough to admit a word correctly without loading `design:lexicon`. Point at the skill instead.
- **Some wording does not move a run.** Several rewordings aimed at Tileand's `ExitRequested`-shaped openings changed nothing: runs never looked at those clauses in a 500-line, well-commented file. Several aimed at *shortcut* and *driver* changed nothing either; both are now accepted either way. A sentence telling runs that a test file's summary of its tests goes took reasons and fixture descriptions with it, and was taken out.
- **A headless run ends when the session ends its turn.** A reviewer launched in the background, a re-review or a timer, can leave the run's last message an interim one. The review cycle now says to wait for every reviewer; the timer artifact remains.

## Runner facts

Established by probe, not in the runner's documentation:

- `--case` is not repeatable (the last one wins) and takes plain `*` wildcards only; use one glob, or `--tag`.
- A `plugins:` entry may not point at a directory beside the cases, so a case that ships its own plugin copy keeps it in its own subdirectory.
- Three dashes in a row anywhere in a grader's frontmatter, comments and patterns included, end the frontmatter, even mid-line, and the case then fails to load. In a pattern, write `-{3}`.
- A scaffold script gets a scrubbed environment, and a case cannot be skipped: see [The Tileand case](#the-tileand-case).
- Resumed runs: see [Resumed interviews and their transcripts](#resumed-interviews-and-their-transcripts).
- Every run starts with `--permission-mode dontAsk`: see [Guard cases](#guard-cases).

## Tools

`evals/tools/` holds what was needed to build and debug this suite and will be needed again. All run from the repository root; each file's header says more.

| Tool | Use |
|---|---|
| `show-run.py result.json` | One line per run of a `--json` result, with the graders that failed and each run's `error`, which is where a usage-limit failure shows. |
| `show-turn.py <trace.jsonl>` | What a run did, in order, from a trace kept with `--keep-temp`: each tool call and each message. |
| `clean-kept-runs.py result.json` | Removes the run directories a finished pass kept, and only those. They hold directories sealed at mode 000, so plain `rm` fails, and a wildcard would hit runs still in progress. |
| `make-history.py`, `extend-history.py` | Build the transcript a resumed case needs (`context.history_file`) from the runner's own output: the first from a kept run's stored session, the second one exchange at a time from each resumed run's trace. They strip machine paths and refuse to write a history that still has one. Follow with `evals/refresh-histories.py`. |
| `sync-calibration-rubrics.py` | Copies each `llm` grader's rubric into its calibration cases; `--check` exits 1 if a copy differs, and it names any `llm` grader that has no calibration case. |
| `lexicon-graders/` | The regex graders of the four invented lexicon fixtures as one table (`gen-graders.mjs`), an offline test of every pattern against a hand-made correct output and the untouched fixture (`test-graders.mjs`, with `samples/`), and a check that the files on disk match the table (`check-files.mjs`). Change a pattern in the table, test it, then `gen-graders.mjs write`. The generator leaves existing `llm` graders alone: their rubrics are calibrated and edited by hand. |

Not kept: the one-off scripts that built the ADR, `philosophy-*`, `interview-*` and calibration cases. Those cases are plain files now; edit them by hand. The Tileand cases' graders are generated from the owner's labels by scripts that live with the labels, outside this repository.
