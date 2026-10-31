# Evals

The eval suite of the marketplace's two plugins, `design` and `implementation`, run with Claude Code's own runner, [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). It lives at the repo root rather than inside a plugin, so it never ships with one: the marketplace installs `./plugins/design` and `./plugins/implementation` and nothing outside them.

## Before you change a skill because of a result here

**Four cases are held out: `lexicon-tessera` and `lexicon-byre` for `design`, and `review-heldout-quarry` and `code-style-heldout-cinder` for `implementation`. Look at their scores. Never edit a skill in response to a specific failure on one.** They exist so that there is always an input no iteration of the skills was tuned on, and they are the only evidence that a change generalised rather than fitted the cases it was tuned against. The first skill edit made to fix a Tessera or Byre failure spends that, for good: the case becomes a regression fixture like the others, and a new held-out one has to be built by an agent that has seen neither the skill nor the other fixtures.

What to do instead, when a held-out case shows a real defect: plant the same kind of trap in a regression fixture (`lexicon-shelfwise`, `lexicon-stockroom` for the lexicon; the ferry fixture for the review cycle; `code-style-lockerline` or an authoring case for code-style), iterate the skill against that, word the change as a general rule, and read the held-out case again afterwards.

Every other case is a regression case and fair to iterate against, the lexicon's Tileand case included. `code-style-tileand` is the exception the other way: a read-only check of what the skill makes of real code, never iterated against (see [Code-style cases](#code-style-cases)). Fixing a grader, a rubric or an answer key because it was wrong is always allowed, on held-out cases too: the rule is about the skills' text. The reasoning, and why there are two, is under [Held out](#held-out).

## Run

From the repo root:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none
```

The repo root has no `plugin.json`; each case names the plugin under test itself, with `plugins: ["../../plugins/design"]` in its frontmatter. An `implementation` case lists both plugins: the runner enforces `dependencies`, and a plugin whose dependency is not loaded does not load (established by probe on Claude Code 2.1.302). `--eval-dir` can't do this, since it only accepts a directory below the plugin.

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

`--scaffold` runs each case's `scaffold.sh` as you, outside the sandbox; it only copies the case's `fixture/` into the workspace. `--allow-tools` applies to every case in the run, so pass it with `--tag fixture` rather than on a smoke run. Of the `design` cases none needs Bash; the review-cycle cases do, and need the sandbox backend (`bubblewrap` and `socat`): see [Review-cycle cases](#review-cycle-cases).

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
| `adr-partly-superseded-other-format` | one of two decisions in an old-format record changes: one new record names the decision it takes over, the old one stays Accepted and is marked partly superseded in its own field, nothing is split |
| `adr-no-directory` | with no ADR directory, it asks where, suggests a concrete place and creates nothing |
| `adr-boundary-says-enforced` | a decision that draws a boundary, with an architecture test beside it, ends its Decision with the fixed sentence that says so; `adr-new-record` and `adr-title-states-decision` check that a record drawing no boundary does not |
| `philosophy-before-implementation` | `design-philosophy` loads, by its qualified name, before the first edit of a request that adds behaviour |
| `philosophy-not-for-mechanical-edit`, `philosophy-not-for-rename` | it does not load for a typo fix or a rename |
| `philosophy-before-seeding` | in a design interview resumed at the scope confirmation, it loads before the tree is seeded |
| `interview-component-not-admitted` | a branch closes by introducing a module and a class: `design-interview` admits nothing to the lexicon |
| `interview-inherited-entry-unchanged` | a branch decides how an inherited concept is shown, not what it means: the inherited entry stays as it is |
| `interview-narrower-meaning-admitted` | a branch fixes what a word means: it is admitted, by meaning not mechanism, after `design:lexicon` is loaded |
| `interview-oversized-lexicon-noted` | a 34-entry lexicon is noted at ingestion and consolidation offered as separate work, not done |
| `interview-lexicon-write-back` | after the wrap-up, the lexicon is written back: inherited entries byte-identical, new terms as entries, and the reply says what is new and what changed |
| `interview-boundary-closure-names-test` | a branch closes by placing a module and saying who may import it: the closure decides the architecture test that protects that boundary, and the threshold branch closed beside it gets none |
| `interview-brief-carries-boundary-test` | after the wrap-up, capture carries that test into the brief's acceptance criteria and the boundary's ADR carries the enforcement sentence |
| `trigger-ready-for-pr` | `implementation:review-cycle` loads when a branch is ready for its pull request, without being named |
| `trigger-not-for-open-pr` | it does not load for reviewing a pull request a colleague opened |
| `cycle-asks-for-brief` | with no brief and no tracker, it asks for the brief and launches no reviewer |
| `cycle-feature` | a feature: lenses chosen by signal (platform reality through the assumptions record), repo lenses that extend, stand alone or do not match, general-purpose reviewers on the session's model, the base read from `origin/HEAD`, test-first fixes, the class sweep under the default out-of-scope policy |
| `cycle-fix-defers` | a small fix: adversarial and design parity only; the repo's own out-of-scope policy overrides the default |
| `cycle-records-only` | a change of records only: design parity in records-only mode, no suite, the brief checked against itself |
| `lens-ferry` | the lenses on the seat-holds branch, stopping after triage: nine planted defects caught, two traps not flagged |
| `cycle-protected-trace` | with a protected-paths list, each protected change in the diff traced to an approved closure: a lens edit approved as P1 is traced to it, an ADR whose closure was declined is a finding in the fixed phrase. Stops after triage |
| `review-heldout-quarry` | the same on a fixture built by an agent that never saw the skill: ten defects, three traps. Held out: see below |
| `code-style-before-implementation` | `implementation:code-style` loads before the first edit of a feature, beside `design-philosophy` |
| `code-style-for-rename`, `code-style-for-comment-pass` | it loads for a rename and for a pass over docstrings, where `design-philosophy` does not |
| `code-style-not-for-typo` | it does not load for a typo in prose |
| `code-style-authoring-scale` | writing code over a device: its one non-local protocol fact is said; nothing restates; domain words from the lexicon; names say what things are |
| `code-style-authoring-contract` | a new public function whose callers must honour a precondition from outside the code: it is on the function |
| `code-style-authoring-stale` | a change that makes an existing comment false: the false claim does not survive |
| `code-style-authoring-decision`, `-test`, `-plain` | guards: a reason kept out of an ADR is said beside the code; tests cite no record where the project bars it; a helper with nothing to say gets no comment |
| `code-style-lockerline` | a comment pass over an invented Java project with 30 planted comments: deletes, shrinks, keeps and three citation regimes |
| `code-style-heldout-cinder` | the same on a Rust project built by an agent that never saw the skill. Held out: see below |
| `code-style-tileand`, in `evals-tileand/` | the same on Tileand's `Hosting/` at `0e71d66`, graded against labels kept outside this repository. A read-only check: see [Code-style cases](#code-style-cases) |

The smoke cases grade only `tool_used: Skill`, which can't pass without the plugin, so a baseline arm would tell them nothing beyond "the skill fired".

## ADR cases

The `adr-*` cases run on Tidewatch, an invented project with a small ADR directory: records 0001, 0002 and 0004, so the gap at 0003 is there to be filled by mistake. Like the lexicon fixtures they copy a `fixture/` into the workspace and write files, so they need `--scaffold --allow-tools Write Edit`; `--tag adr` runs them alone. They are cheap: a run takes under a minute, and the first seven at three runs each took about four minutes at `-j 4` and reported $5.86.

Nearly everything is graded from the files the run leaves behind. Where a case needs a known file name to read a new record back, the prompt gives the title to use; `adr-title-states-decision` leaves the title to the skill, and one narrow `llm` grader reads the created file's name.

The supersede cases carry two graders on the new record: `new-names-what-it-supersedes`, that it has a `**Supersedes:**` link at all, and `supersedes-on-the-status-line`, that it sits on the status line after a middle dot, as `references/format.md` lays the header out. Under design 0.5.1, seven of eighteen runs put it on a line of its own: only the reference file said where the field goes, and a run that did not open it had nothing to go on. 0.6.0 says it in `SKILL.md` and shows the whole line, and the three cases passed in all 27 runs made on it. The split case run beside them, `adr-partial-supersede-split`, passed in all seven; it tested a split rule the skill has since dropped, and became `adr-partly-superseded-other-format`. Nothing else in the ADR cases failed once the graders were right.

0.7.0 added the partly superseded form, in which the old record keeps `Accepted` and gains a clause, and from then on some runs left a wholly superseded record Accepted with the new status beside it: `Accepted. Superseded by ADR-0005`, or `Accepted; superseded by …`, the partial form's shape. Over eight runs `adr-supersede-status-section` passed 5 times on 0.9.0 and 6 and 7 times on 0.10.0, and in one more passing run the old record was written that way first and then corrected. The full-supersede rule said where `Superseded by` goes but not that it replaces what was there. 0.10.1 says so, and that only a partial supersede keeps the status: the four supersede cases then passed in all 32 runs, and no run wrote `Accepted` beside `Superseded` even on the way.

The files are generated; the generator is not kept here. Edit them by hand.

## When design-philosophy loads

The `philosophy-*` cases check that `design-philosophy` loads when it should and only then. All are deterministic: `tool_used` on the `Skill` call, and a `regex` over the session trace for order, written so that one pattern covers a run that edits a file and a run that rewrites it whole. `--tag philosophy` runs the four; they need `--scaffold --allow-tools Write Edit`. 

The failure these guard against is intermittent, so read them over several runs rather than one. Under design 0.5.1, over eight runs each: `philosophy-before-seeding` passed eight times and `philosophy-before-implementation` twice; the two "not for" cases never failed in three. Against the plugin as released at 0.5.0 `philosophy-before-implementation` passed in none of five runs. Where it fails, the skill is never called at all: the request is carried out without it.

Under design 0.6.0, whose description names the moment and the size of the work the skill loads for, `philosophy-before-implementation` passed in all eleven runs, `philosophy-before-seeding` in all seven, and the two "not for" cases in all seven each.

THE-222 moved the comment rule ("Comments justify, code describes") out of `design-philosophy` into `implementation:code-style`, keeping the boundary heading and the sorting test. On the edited text the four cases passed in all eight runs each, and the `interview-*` cases, whose histories embed the skill's text and were refreshed, in 14 of 15.

A fifth case, `philosophy-before-next-closure`, was removed (THE-206). It resumed an interview whose tree had been seeded without the principles, a state 0.5.0 could produce and later versions do not: `philosophy-before-seeding` has not failed since 0.5.1. It passed about half the time, and four rewordings of `design-interview` did not move it.

### Resumed interviews and their transcripts

`philosophy-before-seeding` and the `interview-*` cases resume a conversation (`context.history_file` in `case.yaml`), and the case's prompt is the user's next turn. Established by probe on Claude Code 2.1.278, since the documentation says none of it: a history needs only `user` and `assistant` records chained by `uuid` and `parentUuid`; the trace of a resumed run holds only its new messages, so an order check sees exactly what happened after the resume; and a resumed run saves no session file in its kept run directory. Instead it writes the resumed session into the case directory, beside `history.jsonl`, in a file named by the history's session id, and appends to it on every run. Each run still starts from `history.jsonl` alone, so runs do not see one another; the file is gitignored so that `git status` stays clean after a run.

The transcripts are of an invented project and were produced by the runner itself: a run's stored session (under `config/projects/` in a kept run directory) was cut down to the conversation, and each later turn was appended from the next run's trace, with the user's replies written by hand.

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

Under design 0.5.1, over eight runs each unless said: the component was never admitted (three of three), the inherited entry never touched (eight of eight), the write-back correct (three of three). `interview-narrower-meaning-admitted` passed four times in eight, and failed the same way each time: the word was admitted, by meaning, but `design:lexicon` was never loaded, though the interview skill says to load it before the first admission. The interview carried its own one-sentence summary of the three tests, which was enough to admit a word correctly without the skill. 0.6.0 takes that summary out, so the tests live only in `design:lexicon`: the case passed thirteen times in fifteen on the released text, the two failures being the same one, and the other four cases in all three runs each. `interview-oversized-lexicon-noted` passed seven times in eight after one grader fix: a correct run had called the 34 entries "40-odd", which the pattern did not accept. Its one remaining failure, on the offer of consolidation, came from a run whose trace was not kept. Eight more runs with traces kept all made the offer, and all in the word "consolidation", which the first pattern accepted; so that failure was most likely a run that did not make the offer, about one in sixteen, not a wording the pattern missed. The pattern had been widened meanwhile to the other natural ways of making the offer, and stays so.

`interview-narrower-meaning-admitted` read low again on 0.9.0 and 0.10.0 (4, 5 and 7 of 8), the same failure each time: *silent* admitted, by meaning, without `design:lexicon`. The rule to load it stood under Admission, but the closure paragraph that a run acts on at the moment it admits said only to admit "against the `design:lexicon` skill's tests". 0.10.1 says there that those tests are not in this skill and to load it before writing the recap. Over 16 runs it loaded in 16; the other four `lexicon-admission` cases, whose histories were refreshed, passed 31 of 32, the one failure `interview-oversized-lexicon-noted` noting the code-name entries but not the size, as before. One of the 16 failed `entry-states-meaning-not-mechanism` on a split vote, and the grader was wrong: the entry defined *silent* by meaning and left the hour and the three readings out as decisions, as `design:lexicon` asks, and the rubric wanted the edges in it. It now accepts either, and says a recap is not an entry.

Two things about the runner found on the way: `--case` is not repeatable (the last one wins) and takes plain `*` wildcards only; and a `plugins:` entry may not point at a directory beside the cases, so a case that ships its own plugin copy keeps it in its own subdirectory.

### Boundaries and their tests

The cases tagged `boundary` (THE-253) check that a boundary is decided together with the architecture test that protects it. A boundary is what `design:adr` says it is: one module's use of another, a surface and the consumers allowed to use it, or a prohibition, where a decision drew it. `--tag boundary` runs the three; they need `--scaffold --allow-tools Write Edit`.

- `adr-boundary-says-enforced` runs on Tidewatch: a decision that the flood page reads levels only through one module, with an architecture test landing beside it. The record's Decision must end with `design:adr`'s fixed sentence, "The architecture tests enforce this boundary.", by regex. `no-enforcement-claim` on `adr-new-record` and `adr-title-states-decision` checks the other direction: a record that draws no boundary never carries it.
- The two interview cases run on `design-fixtures/gaugefeed/` (see the README there): gaugefeed grown into a project whose stdlib architecture test is an allow-list of imports, shared so that THE-241's cases can use it too. Both resume one interview about a station that stops answering for days, chained on design 0.9.0 with the user's replies written by hand. `interview-boundary-closure-names-test` stops where the assistant has asked its probes on where the silence state lives (U1) and on the silence threshold (U2); the prompt closes both and never mentions the architecture test. Two narrow `llm` graders: U1's closure decides what the rule permits or forbids, inside the closure and not as a blast-radius to-do; U2's closure, which no import rule can see, gets no architecture test. `interview-brief-carries-boundary-test` goes on to the wrap-up, the user having stated the test while closing U1, and asks for capture: the brief's acceptance criteria name the test, and the record written for U1 carries the sentence (a regex over the record's `Write` in the trace, since the file name is the skill's to choose).

On design 0.9.0 all three failed every run: no record carried the sentence (3 of 3), no U1 closure decided the test (3 of 3; one named the allow-list entry only under "what closing these changed"), and capture wrote the test into the brief's acceptance criteria in 2 of 3 runs but never into the record. The chained transcript showed the same thing: told the test outright while closing U1, the assistant left it out of U1's recap and filed it under testing strategy.

It took three rounds of wording. The first said it in `design:adr`, in `design-interview`'s closure states and in the acceptance-criteria template; the interview closure passed from then on. The record still failed 3 of 3: capture did not hand the boundary line to `design:adr`, and one run withheld the sentence because the test "lands with the implementation", which the first wording's "lands in the same change" allowed. The second round has capture pass the line on and says a test decided with the boundary counts. Then the acceptance criteria missed the test in 2 of 3: no run had opened the template, so the third round puts the rule in `SKILL.md`'s closure paragraph and keeps in the template only why this one criterion may name structure. On design 0.10.0, over eight runs: `adr-boundary-says-enforced` 8 of 8, `interview-boundary-closure-names-test` 8 of 8, `interview-brief-carries-boundary-test` 7 of 8 (one brief without the test in its criteria).

Two older cases were lower than their recorded rates in the same pass, and an A/B against `master` (design 0.9.0) at eight runs each showed it was not this change: `adr-supersede-status-section` 5 of 8 on 0.9.0 and 6 of 8 on 0.10.0, `interview-narrower-meaning-admitted` 4 of 8 and 5 of 8. Both were the skills' wording, fixed in 0.10.1: see [ADR cases](#adr-cases) and [Lexicon admission inside the interview](#lexicon-admission-inside-the-interview).

The held-out lexicon cases, read after the change though it does not touch `design:lexicon`: Tessera 6 of 8 and Byre 7 of 8, each failure a different grader once.

## Lexicon fixtures

`lexicon-shelfwise`, `lexicon-stockroom`, `lexicon-tessera` and `lexicon-byre` are invented projects whose lexicon is planted so the right answer is known by construction: each entry exercises one of the skill's rules, and the source code decides several verdicts in both directions, with things a correct run must find and decoys it must not fall for. They can be committed because nothing in them is real.

Each case directory holds:

- `fixture/`: the project, copied into the workspace by `scaffold.sh`. Nothing else is copied.
- `expected.md`: the verdict for every entry, the drift at `file:line`, the homeless sentence, the outside edges, the gap and the decoys; then what the graders check, what they leave ungraded and why.
- `graders/`: one deterministic `regex` grader per planted rule, on the written lexicon (entry headings kept or gone, a merge recorded, no entry over 80 words) and on the report (the drift and edge citations, the homeless sentence, the gap). One narrow `llm` grader per case, where a pattern can't decide.

The prompt gives sign-off in advance, since the skill waits for it before writing and a run has nobody to ask.

When writing a grader, keep three dashes in a row out of its frontmatter, comments and patterns included: the runner ends the frontmatter at the first one it meets, even mid-line, and the case then fails to load. In a pattern, write `-{3}`.

Shelfwise and Stockroom are regression fixtures: both were used while the skill's 0.5.0 text was tuned, and each `expected.md` says how. Items that flipped between those tuning runs are graded only where the key and its amendments leave one right answer.

Under design 0.6.0, on the released text and the graders as they stand: Shelfwise passed 55 of 63 runs, Stockroom 10 of 11, Tessera 17 of 19 and Byre 14 of 27. What fails is intermittent and mostly on the report rather than the written lexicon. On Shelfwise, `drift-receipt-cited` (5 of 63) and one each of `no-code-names`, `synonym-recorded-not-used` and `homeless-pilot-sentence`; on Stockroom, *stock* kept as an entry instead of merged into *on-hand* (`synonyms-merged`, about one run in eight on any version).

Two things changed in 0.6.0 that these fixtures measure. A user-facing quantity is no longer retired for having a configuration key: Stockroom's *reservation TTL* was kept in 1 of 8 runs under 0.5.1 and in every run since. And a reframe's entry is now written rather than proposed: *batch* is written and *wave* and *branch* stay gaps in every run.

Two planted words are accepted either way, by the owner's ruling (THE-212): *shortcut* on Tessera and *driver* on Stockroom, each an ordinary word whose documentation also uses it in another sense nearby. Runs keep such a word with its sense stated about half the time or more, four rewordings of the skill did not change that, and the owner's reading is that the ambiguity is the documentation's. Stockroom's *scan*, whose other sense only developers meet, is still graded and has never been kept.

`no-code-names` is worth knowing about. It did not fail in 168 fixture runs before the reframe change and has failed in 4 of 120 since (Tessera 2 of 19, Byre 1 of 27, Shelfwise 1 of 63, Stockroom 0 of 11). Fixture by fixture that is not distinguishable from chance, and 54 further Shelfwise runs with traces kept did not reproduce it, so what the failing runs wrote is not known. If it shows again, keep the trace (`--keep-temp`): the fixtures where it has failed are the ones whose gap word has a component named to avoid it (`BranchSite`, `SecondaryArea`, `Insemination`), and a component named on the gaps line is the first thing to look for.

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

The graders are the owner's gold labels: `gone-*` and `kept-*` on the written lexicon's entry headings, one per labelled entry, and a few more for what a heading can't express. `expected.md` lists the verdicts and says which came from the owner and which were agreed by default. Both are generated by `gen-graders.py`, which lives with the labels outside this repository, along with the owner's reasons and a test that checks the graders against Tileand's own before and after. Regenerate them rather than editing them. Tileand's own consolidated lexicon fails only the graders of the entries on which the owner's label disagrees with it, which that test checks after every regeneration. A label can move: the owner has changed three since the first labelling, after seeing what runs did and why, and a `README.md` beside the labels gives the steps.

This case is a regression input, like Shelfwise and Stockroom: iterate against it, but word any change to a skill as a general rule that holds for the other cases too, and read the held-out cases afterwards.

Under design 0.6.0, over eight runs, scores ran from 0.92 to 0.97, against 0.86 to 0.93 over four runs of 0.5.1 (both graded against the labels as they stood before three rows moved on 2026-09-20, so a little low). The defect 0.6.0 fixes here is a reframe that stops short: a run decided that a retired component's concept needed a word and then left the entry in its report, awaiting a sign-off the prompt had already given. *reconcile* is now written in 8 of 8 runs (2 of 4 before), *layout* in 4 of 8 (1 of 4) and *rescue* or *rescued end* in 4 of 8 (1 of 4), and no run holds a drafted entry back. What is left is judgement about the word rather than the procedure: the concept lands under *end* or `unhide`, or the run judges *layout* ordinary in this domain.

Several rows of the first table of findings turned out to be the labels rather than the skill, and the owner moved them after reading what the runs did and why: *host window* is a plain retire (runs propose *window* as a gap, which is neither required nor penalised), *default rules* and *attempt schedule* are out of the gold set, *workspace* is accepted with or without its lifecycle clause, and `reframed-rescue` accepts *rescued end*.

## Review-cycle cases

The cases tagged `review-cycle` check `implementation:review-cycle` (THE-251). They were written before the skill was ported, as its specification, and the skill was changed to meet them; a case or grader changes only when it was badly written.

All but the held-out one run on the ferry fixture in `review-fixtures/ferry/`: Ferrybook, an invented car-ferry booking service in Python with stdlib `unittest`. `build.sh` commits a base on `trunk` with a fake `origin/HEAD` naming `trunk` as the remote's default (a cycle that assumes `main` fails visibly), then the case's branch on top: `feature` (seat holds, nine planted defects and two traps), `fix` (a midnight-boundary fix that is itself off by one, with the same bug outside the change for the class sweep), `records` (an ADR that contradicts an accepted one), and a `policy` overlay whose `AGENTS.md` says out-of-scope defects are listed, never fixed. Two more overlays, `protected` on the base and `protected-fix` on top of `fix`, are seen only by `cycle-protected-trace`; `build.sh` takes comma-separated overlay lists for that. The base carries three repo lenses under `.claude/skills/`, each with a phrase found nowhere else, so a grader can see whose prompt a lens's body reached. `expected.md` beside the fixture has the answer key.

`review-heldout-quarry` is a quarry blasting scheduler built by an agent that saw neither the skill nor the ferry fixture, from a list of defect kinds only. It has no remote, so it also covers the base branch when there is no `origin/HEAD`.

Run them with Bash granted, and with the Python documentation reachable, since the platform lens checks claims against it:

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold \
  --tag review-cycle --allow-tools Bash Write Edit "WebFetch(domain:docs.python.org)"
```

Leave Bash out for `--tag trigger`: the trigger cases list no `Agent` and stop at six turns, since all they need to see is the Skill call. A Bash-granting run is refused outright, scoring 0 at no cost, while `~/.docker` holds a symlink, which Docker Desktop's WSL integration creates; `DOCKER_CONFIG` does not get round the check, and the links have to become plain copies.

They are the suite's dear cases. A `lens-*` run takes about ten minutes and reports about $6; `cycle-feature` takes up to half an hour and about $12, since it reviews with five reviewers, fixes test-first and re-reviews. One run of every review-cycle case is about $35 to $40. Run the cases a change touches, not the tag; `--tag full` is the three cycle cases that fix, `--tag lens` the two that stop after triage.

What the graders read: lens selection and repo lenses from the `Agent` calls' prompts (`tool_used` with `input_match` on each lens brief's heading); the base and the suite from `Bash` calls; fixes and the sweep from the files; defects caught from the final report, by regex where a finding has a distinctive identifier and by a narrow, calibrated `llm` grader where it is a judgement. A subagent's own tool calls are in the trace and counted by `tool_used`, and each of its trace lines carries its parent's `"parent_tool_use_id":"toolu_…"` (the main session's carry `null`), which is how `cycle-records-only` tells a reviewer's suite run from the session's.

Results, with `claude-opus-5`, by the skill text each run used:

| Case | First port (`2619725`) | Table and mode fixes (`e39d99a`) | Waits for its reviewers (`3841fba`) |
|---|---|---|---|
| `trigger-ready-for-pr` | 1/1 | 2/2 | |
| `trigger-not-for-open-pr` | 1/1 | 2/2 | |
| `cycle-asks-for-brief` | 1/1 | 2/2 | |
| `cycle-feature` | 1/1 | 1/2 | 2/2 |
| `cycle-fix-defers` | 1/1 | 2/2 | |
| `cycle-records-only` | 0/1 | 3/3 | |
| `lens-ferry` | 1/1 | 2/2 | 3/3, on the subtler D1 |
| `review-heldout-quarry` | 1/1 | 2/2 | |

What the runs taught, in the order it happened:

- **The table is the whole selection.** The first records-only run added platform reality on its own judgement, because the new ADR stated a fact about rounding; and its design-parity re-run lost the records-only mode. `e39d99a` says the table is the whole selection, a re-run keeps its mode line, and records-only design parity checks a record's platform facts against the documentation itself.
- **A change can stop being records-only.** The default out-of-scope policy lets the class sweep fix a float in `child_fare`, after which a second round rightly runs the suite. `cycle-records-only`'s no-suite and not-selected graders judge the first round only: every reviewer launched before the session's first edit.
- **Reviewers may run in the background.** One `cycle-feature` run launched its re-review, which ran in the background, wrote its report as an interim message and ended its turn; the headless run ended there. `3841fba` says to wait for every reviewer, the re-run included, and not to end the turn while one is running.
- **D1 was given away.** `_new_ref` carried the comment "Keep references short", echoing the alternative ADR-0001 rejected, and a `cycle-asks-for-brief` run spotted it while only gathering context, before any reviewer ran. The comment is gone; `lens-ferry` finds D1 from the code against the ADR in three runs of three.
- **Graders that were wrong:** `review-heldout-quarry`'s D7 wanted the identifier `notified_receptors` where a correct run described the decision ("the outbox says who was told"); `asks-for-the-brief` failed a run that asked and offered one observation provisionally, which the case never meant to fail; `report-gives-dispositions` did not say an interim report fails. All three were corrected, the two rubrics recalibrated.

What the runs found that no grader asks about, and worth knowing: the sessions found real defects in the ferry fixture that were not planted (waitlist promotion bypasses the capacity check; a refused second hold destroys the first), which `expected.md` does not list and nothing penalises; they try to push and open the PR, which the sandbox refuses; and they write `.claude/skills/` only where the sandbox lets them, so a stale repo lens's globs are reported rather than fixed.

**`cycle-protected-trace`** (THE-252) guards step 1b, the trace of protected changes the cycle runs itself. The `protected` overlay puts `.claude/protected-paths.txt` on `trunk`; `protected-fix`, on top of `fix`, adds a midnight attack to the `ferry-attacks` lens, which the brief's batch approves as P1, and a correct new ADR with its index row, which the batch proposed as P2 and the maintainer declined. It stops after triage, and its three regex graders read the report: the fixed phrase `Protected change without an approved closure:` on the ADR's line, never on the lens's, and the lens's line naming P1. On the skill before the step, 0 of 2 (a third run died on an OAuth error): both runs reported the declined ADR in their own words, never in the fixed phrase. With the step: 2 of 3, then 2 of 3 and 6 of 8 once the phrase had to be written exactly, path after the colon (a table had put the path in one column and the phrase in another), and 7 of 8 with step 2's sentence on wait timers. Every failure after the phrase fix was the same artifact: the report was right, but a background `sleep` the session had started to keep its turn open while reviewers ran finished after it, so the last message was a note about the timer. Stopping the timer does not prevent it, since a stopped task's notice still arrives later. `review-heldout-quarry`, read once afterwards, scored 0.375 for the same reason; its nine regex graders all match the real report. `cycle-fix-defers` 2 of 2 and `lens-ferry` 2 of 2 on the same text. Reported cost of all of it, red runs and regressions included, $74.

## Code-style cases

The cases tagged `code-style` check `implementation:code-style` (THE-222). Like the review-cycle cases they were written before the skill, as its specification, and list both plugins, since `implementation` depends on `design`. They need `--scaffold --allow-tools Write Edit` and no Bash.

```sh
claude plugin eval . --model claude-opus-5 --judge-model claude-opus-5 --ablation none --tag code-style --scaffold --allow-tools Write Edit
```

**Authoring first.** The skill is loaded while code is written, not run over it afterwards, so the cases that matter most give the agent a task and grade the comments and names that come out. They run on `roastlog`, an invented coffee-roastery log in Python, and **with the baseline arm** (omit `--ablation none`): a skill that made agents comment more would show as a negative Δ on the restatement graders, which a count of comments would reward. Each case grades both directions: the one fact from elsewhere that the task makes the agent discover is said, by a regex on its meaning; nothing added only restates the name, signature or code in view, by a narrow llm grader. `decision`, `test` and `plain` pass without the skill too and stand as guards.

**Audit second.** `code-style-lockerline` (Java) and `code-style-heldout-cinder` (Rust) plant comments whose right answer is known by construction: deletes, shrinks, and mostly keeps, as real code is. Graders score over-deletion and under-deletion apart: a regex per keep and per delete, the local half of each shrink gone and its non-local half kept, and one llm grader per shrink whose surviving sentence can break (a stranded pronoun, a scope qualifier cut, a why turned into a false what), plus "nothing added". `AGENTS.md` sets three citation regimes, as Tileand has: `src/` cites by number, `tests/` cites nothing, a structural-tests folder cites beside its own words.

**Graded in proportion** (owner, 2026-10-19: "we're not building a banking agent, we're building a code-style skill"). Where a result has more than one reasonable form, every reasonable form passes: a light restatement left in because it gives the next clause its subject, a comment deleted whose content is plainly in the code beside it, a shrink that capitalises its new first word (every phrase grader is case-insensitive). What is always failed: pure restatement kept, context from elsewhere lost, a claim added, a reference stranded, a citation where the project bars one.

**`code-style-tileand` is a check, not a target.** It runs the audit on Tileand's `src/Tileand.Core/Hosting/` and `tests/Tileand.Tests/Hosting/` at `0e71d66`, the commit before THE-221's comment pass, brought in at run time like the lexicon case (`evals-tileand/tileand-repo.path`). It shows what the skill makes of real code; it does not define proper code style, and the skill is never reworded because of a result on it. Its labels live outside this repository: THE-221's changes, and 25 verdicts Claude made from runs' unlabelled deletions and the owner agreed. A comment THE-221 left alone is unlabelled, not a keep, since the owner ruled that pass triage. Its graders and `expected.md` quote Tileand's comments, so they are generated locally (`~/lexicon-eval-fixtures/tileand-comments/gen-graders.py`) and gitignored; without them the scaffold fails at once, for free, saying so. It has no llm graders: its files run to 24 kB, where the judge is noisy.

```sh
claude plugin eval . --eval-dir evals-tileand --case code-style-tileand --model claude-opus-5 --judge-model claude-opus-5 --ablation none --scaffold --allow-tools Write Edit --runs 3
```

Under the skill as merged, over eight runs (authoring with the baseline arm beside it):

| Case | With the skill | Without |
|---|---|---|
| `code-style-before-implementation`, `-for-comment-pass`, `-not-for-typo` | 8/8 each | |
| `code-style-for-rename` | 7/8 | |
| `code-style-authoring-contract` | 8/8 | 0/8 |
| `code-style-authoring-scale` | 7/8 | 3/8 |
| `code-style-authoring-stale` | 8/8 | 7/8 |
| `code-style-authoring-decision` | 7/8 | 7/8 |
| `code-style-authoring-plain`, `-test` | 8/8 each | 8/8 each |
| `code-style-lockerline` | 8/8 | |
| `code-style-heldout-cinder` | 2/8 and 3/8 in two confirmations, scores 0.94 to 1.00 | |
| `code-style-tileand` (three runs) | scores 0.78 to 0.80 | |

What it took to get there, worth knowing before changing the skill:

- **The rename trigger.** A rename first failed to load the skill in all three runs: a rename looks mechanical, and the description led with feature work. Leading with names and comments fixed most of it (4/4, then 7/8); the last step was saying that a rename counts even when the new name is given, since the comments naming the old thing go stale (6/8 before, 7/8 after).
- **The interface comment.** The skill's first authoring rule fired only after a lookup ("if writing a line made you look something up, say it"), and `authoring-contract` found the other half missing: a new public member whose callers need a precondition the signature cannot carry. One sentence asking what a caller must know took it from 2/3 to 8/8; without the skill it is 0/8.
- **What did not work.** Four rewordings aimed at Tileand's `ExitRequested`-shaped openings ("An end was requested and…") moved nothing: runs did not judge those clauses non-local, they never looked at them in a 500-line, well-commented file. Two of those rewordings are gone again; the openings are now accepted whole, in proportion. A sentence telling runs that a test file's summary of its tests goes took reasons and fixture descriptions with it, and was taken out.
- **Graders that were wrong:** a keep that required a clause restating its test's name; a stale-claim pattern that also matched the correct rewrite's "until it is weighed"; case-sensitive phrases that failed a correct shrink's new capital; cinder's "nothing added" rubric, which did not say a cut or a near-synonym is not an addition.

## Held out

Tessera and Byre are held out, so that there are always inputs no iteration of the skill was tuned on. Each was built by an agent that had seen neither the skill nor the other fixtures, from a list of defect kinds only. They stay held out under one rule: look at their scores, but never edit the skill in response to a specific failure on one. Iterate on Shelfwise, Stockroom and the Tileand case; read Tessera and Byre as the check that the iteration generalised. `--tag held-out` runs the two alone. Once a failure on one of them has shaped the skill's wording, that one is a regression fixture like the others and a new held-out one is needed.

`review-heldout-quarry` is held out for `implementation` under the same rule, with the ferry cases as its regression fixtures. So is `code-style-heldout-cinder`, with `code-style-lockerline` and the authoring cases as its regression inputs; it was built before any of the code-style skill's text existed, and its graders were checked and calibrated by a second fresh agent, so that nobody who has read its answers has worded the skill. `--tag held-out` runs all four.

There are two lexicon ones because they catch different things. Tessera is a tiling window manager, the same kind of system as Tileand, which the skill was first tuned on: it shares none of Tileand's text, so it catches fitting to Tileand's wording and structure, but it is weaker at catching fitting to that domain. Byre, dairy herd management, shares nothing with any other input here.

Read Byre over a dozen runs or more. It passes about six runs in ten on any version (11 of 18 on 0.5.1, 14 of 27 on 0.6.0), on the same few graders each time: `distinction-milking-names-session` and `forty-day-sentence-home` fail in about one run in four or five each, `drift-withdrawal-cited` in about one in nine. Three runs say nothing: 0.5.1 passed three of three when the fixture was built, and 0.6.0 passed none of three in one suite pass and nine of twelve in another. Tessera is steadier, and since *shortcut* became accepted either way it passes in most runs.

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
| `entry-states-meaning-not-mechanism` | `interview-narrower-meaning-admitted` | 6 | 30/30, 2026-10-31, after rewording and a known pass with the thresholds left out of the entry | 0 | 0 |
| `does-not-consolidate` | `interview-oversized-lexicon-noted` | 4 | 20/20 | 0 | 0 |
| `says-what-is-new-and-what-changed` | `interview-lexicon-write-back` | 4 | 20/20 | 0 | 0 |
| `boundary-closure-names-its-test` | `interview-boundary-closure-names-test` | 5 | 15/15, three gradings each, 2026-10-31 | 0 | 0 |
| `threshold-closure-carries-no-architecture-test` | `interview-boundary-closure-names-test` | 5 | 15/15, three gradings each, 2026-10-31 | 0 | 0 |

The review-cycle graders, calibrated on 2026-10-18 with three gradings each. Their known passes are real final reports judged by hand; their known fails are the same reports with one finding removed or one added that the rubric fails:

| Grader | Case | Outputs | Agreement | Flips | Split votes |
|---|---|---|---|---|---|
| `asks-for-the-brief` | `cycle-asks-for-brief` | 5 | 15/15 | 0 | 0 |
| `report-gives-dispositions` | `cycle-feature` | 6 | 18/18, after one known fail was rebuilt; 15/18 before | 0 | 0 |
| `d2-confirm-without-settling` | `lens-ferry` | 5 | 15/15 | 0 | 0 |
| `t1-lazy-expiry-not-flagged` | `lens-ferry` | 5 | 15/15 | 0 | 0 |
| `t2-replacement-not-flagged` | `lens-ferry` | 5 | 15/15 | 0 | 0 |
| `d1-refused-postpone-leaves-state` | `review-heldout-quarry` | 5 | 15/15 | 0 | 0 |
| `t1-inclusive-window-end-not-flagged` | `review-heldout-quarry` | 5 | 15/15 | 0 | 0 |
| `t2-no-vibration-recheck-not-flagged` | `review-heldout-quarry` | 5 | 15/15 | 0 | 0 |
| `t3-revised-notice-recipients-not-flagged` | `review-heldout-quarry` | 5 | 15/15 | 0 | 0 |

The code-style graders, calibrated on 2026-10-18 and 19 with three gradings each. Known passes are real runs' files, judged by hand (cinder's by an agent that never saw the skill); known fails are the same files with one change: a restating comment added, a function renamed to a vague verb, a stranded "It", a lost reason, a purpose turned into a false behaviour, an added claim:

| Grader | Case | Outputs | Agreement | Flips | Split votes |
|---|---|---|---|---|---|
| `authoring-scale-no-restating-comment` | `code-style-authoring-scale` | 4 | 12/12 | 0 | 0 |
| `authoring-scale-names-say-what` | `code-style-authoring-scale` | 4 | 12/12 | 0 | 0 |
| `authoring-decision-no-restating-comment` | `code-style-authoring-decision` | 4 | 12/12 | 0 | 0 |
| `authoring-test-no-restating-comment` | `code-style-authoring-test` | 4 | 12/12 | 0 | 0 |
| `authoring-plain-no-restating-comment` | `code-style-authoring-plain` | 4 | 12/12 | 0 | 0 |
| `lockerline-shrink-door-latched`, `-held-for-inspection`, `-code-scanned`, `-fan-out`, `lockerline-nothing-added` | `code-style-lockerline` | 4 each | 12/12 each | 0 | 0 |
| `cinder-nothing-added-controller` | `code-style-heldout-cinder` | 6 | 18/18, after one rubric revision (cuts and near-synonyms are not additions); 16/18 before | 0 | 0 |
| `cinder-nothing-added-schedule`, `-shrink-cone-judged`, `-trap-cooling-reason-judged` | `code-style-heldout-cinder` | 5 each | 15/15 each | 0 | 0 |
| `cinder-shrink-run-window-judged` | `code-style-heldout-cinder` | 8 | 24/24, after one revision | 0 | 0 |
| `cinder-trap-heating-scope-judged` | `code-style-heldout-cinder` | 4 | 12/12 | 0 | 0 |
| `cinder-trap-fault-count-reference` | `code-style-heldout-cinder` | 6 | 17/18 | 1 | |

`cinder-trap-fault-count-reference` is below the bar, on purpose: its one flip is a known fail whose kept clause strands a pronoun, a borderline form no run has produced. A stranded reference is one of the few things the code-style graders always fail, so the known fail stays and the grader is read with that in mind, rather than revised a third time or relieved of its hardest case. `code-style-tileand` has no `llm` graders: its files run to 15–24 kB, where the judge is noisy, and shrink quality is covered here.

`report-gives-dispositions`' first calibration was the judge being right: a known fail with its headings stripped still said, finding by finding, what had been done.

What calibration found was in the rubrics, not the judge. Writing down known verdicts for the three sentence-home graders showed that their rubric said both PASS and FAIL of a report that names the true home and the decoy together, which a real Tessera run had done and the judge had passed; and that it named a whole file as the decoy where only one doc comment is, which would have failed a real Byre run for citing the code that implements the behaviour. Then the first full run showed one grader flipping on a real output, because "at or around lines 49-50" left the judge to decide whether line 54 was around line 49. The rubrics now identify the decoy by quoting the comment. A rubric that can be read two ways is where a judge's noise comes from.

It is not cheap. A grading is three judge votes over the whole output, and judging a file reported about ten times the cost that judging a run's last message did in the ordinary suite: the full run of 250 gradings took three minutes and reported $70, and the two long-report graders alone $29. Calibrate one grader at a time with `--tag <grader>` after changing its rubric, and use `--runs 3` unless flips are what you are looking for.

Not covered yet: the owner's Tileand labels. The lexicon's Tileand case has no `llm` graders, so there is nothing of it to calibrate; if narrow `llm` graders are added there for rewrites and reframes, the owner's one-line reasons in the private label file are the known verdicts to build their calibration outputs from.

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
