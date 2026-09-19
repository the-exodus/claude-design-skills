# Byre: answer key

## 1. Header

- Fixture root: `fixture/`, beside this file. All paths below are relative to it.
- Glossary: `docs/glossary.md`, 22 entries (lines 9 to 51, one entry on every odd line).
- The three tests:
  1. **Language, not code.** A term is admitted for what people say about using or developing the system, not because a part of the code bears the name.
  2. **Needs defining.** Someone talking about the system would otherwise misunderstand or lack the word; ordinary words in their ordinary sense, and words whose only content is a decision about behaviour, do not qualify.
  3. **One word per concept.** Synonyms merge under the word actually used (the other recorded as not used); distinct concepts stay distinct and each names the other.
- An entry states meaning and distinctions only: no mechanism, config keys, history or component names; about fifty words at most.
- What is wrong with the glossary's header (`docs/glossary.md:3-5`):
  - Line 5, the admission sentence, is wrong: "A term earns an entry when the team has given something a name, whether in the code or in a decision record" admits code names (fails test 1) and decision-only names (fails test 2). It should state the three tests.
  - Line 4, `Gaps: none.`, is false: "service" is used throughout and never defined (section 7).
  - Line 3, the provenance line, is acceptable as provenance, but it describes the cause of the sprawl ("an entry has been added with each pull request that introduced a name"); it should be updated to record the prune.

Verdict vocabulary used below: **retire** (entry goes), **reframe** (headword goes, the user-facing content survives under another name or home), **merge** (folded into another entry, recorded there as not used), **rename** (meaning stands, headword changes), **rewrite** (headword stands, definition substantially replaced or cut), **keep** (headword and meaning stand; a light edit may be noted).

## 2. Entries

| Line | Entry | Plant | Verdict | Test | Why, with evidence |
| --- | --- | --- | --- | --- | --- |
| 9 | cow | sound term | keep | 2 | Has a specific sense against *heifer* (has calved at least once): `internal/herd/animal.go:43-46`, `README.md:9-10`. Already names *heifer*. No edit needed. |
| 11 | days in lactation | headword drift | rename to **days in milk** (DIM may be recorded as also said) | 3 | No source uses the headword; it occurs only at `docs/glossary.md:11` and `:27`. Every source says "days in milk": `README.md:14`, `docs/configuration.md:23` and `:61`, `docs/decisions/0003-dry-off-date-from-expected-calving.md:9` and `:23`, `internal/lactation/lactation.go:37-39` (`DaysInMilk`). Definition is sound. |
| 13 | dry off | sound term, component reference | keep (light rewrite) | 1 for the cut | Real domain verb and event (`README.md:16-17`, `internal/lactation/lactation.go:83-85`). Drop the sentence "`LactationService` records it and closes the lactation." Keep the pointer to *dry period*. |
| 15 | dry period | bloated | rewrite (trim to the first two sentences) | 2 | Correct term, 155-word definition carrying a config key, two component names, behaviour, a decision's consequence and history. See section 5. |
| 17 | Env | pervasive identifier | retire | 1 | A context object: `internal/env/env.go:48-55`, used in 10 of the 11 Go files and prescribed at `docs/conventions.md:20-21`. Nobody says "Env" when talking about the herd or the system's behaviour. Frequency in code is not a reason to keep. Edge: `internal/env/env.go:49`. |
| 19 | farm | ordinary word | retire | 2 | Ordinary sense everywhere (`README.md:3`, `docs/configuration.md:11`); single-farm install, no tenant or multi-herd sense anywhere. Italicised at `docs/glossary.md:17`, `:43`, `:47`; those italics go. Mildly arguable only on the grounds that three entries lean on it; that is not a reason. Not marked debatable. |
| 21 | GroupManager | concept and component (the component) | retire | 1 | A type: `internal/herd/group.go:29-33`. The concept it realizes is *management group* (line 35), which stays. |
| 23 | heifer | redirect stub hiding a distinct concept | rewrite into a real entry (NOT merge) | 3 | Heifer and cow are distinguished everywhere: `internal/herd/animal.go:38-41` (`IsHeifer`: female, parity 0), `internal/lists/builder.go:39-40` and `:44` (never on the dry-off list), `:69` (maiden heifers go on the serve list by age, not VWP), `internal/herd/group.go:70`, `docs/configuration.md:33`, `:37`, `:43`, `README.md:9-10`. Expected: "A female that has not yet calved; she becomes a *cow* at her first calving." |
| 25 | HerdStore | component name | retire | 1 | A type: `internal/herd/store.go:14-16`. |
| 27 | lactation | sound term, component reference | keep (light rewrite) | 1 for the cut | Drop "*ListBuilder* shows its *days in lactation* beside the cow on every list" (component name, behaviour, and the drifted headword). Meaning sentence stands. |
| 29 | lactation number | synonym, unused word | merge into **parity** | 3 | "lactation number" occurs nowhere but `docs/glossary.md:29`. Code and docs say parity: `internal/herd/animal.go:24-25`, `internal/lactation/lactation.go:24`, `README.md:8`, `docs/configuration.md:22` and `:61`. They are the same number here: a calving raises parity and the lactation it opens carries that parity (`internal/lactation/lactation.go:71` and `:75`). Record "lactation number" under *parity* as not used. |
| 31 | late-reading rule | decision-only | retire | 2 | The name occurs nowhere but `docs/glossary.md:31`; its whole content restates the Decision of `docs/decisions/0002-late-readings-belong-to-their-session.md:21-24`. Behaviour belongs in the decision record (also stated at `docs/configuration.md:12` and `internal/milking/ingest.go:35-37`). |
| 33 | ListBuilder | component name | retire | 1 | A type: `internal/lists/builder.go:22-27`. What users say is "the lists" or the list names. |
| 35 | management group | concept and component (the concept) | keep | 2 | Domain concept users say and configure (`README.md:24-26`, `docs/configuration.md:18`); "exactly one at a time" agrees with `internal/herd/group.go:40-41`. No edit needed. |
| 37 | MeterIngest | component name | retire | 1 | A type: `internal/milking/ingest.go:18-20`. |
| 39 | milking | distinction (the entry missing its pointer) | keep (light rewrite: add "Not a *session*, which is one round of the whole herd") | 3 | Must not be conflated with *session*: `README.md:11-13`, `internal/milking/session.go:27-28`. Only *session* currently names the other. |
| 41 | parity | synonym, the word in use | keep (absorbs "lactation number" as not used) | 3 | See line 29. Cited, correctly, at `internal/herd/animal.go:24`. |
| 43 | session | distinction | keep (un-italicise *farm*) | 3 | Distinct from *milking* and already says so. "Two or three a day" agrees with `docs/configuration.md:11` and `internal/milking/session.go:14-18`. The `Session` struct is only a key (section 8). |
| 45 | user | ordinary word | retire | 2 | Ordinary sense; the only other occurrence is `README.md:45`, also ordinary. No roles, accounts or competing sense anywhere. |
| 47 | VWP | looks technical, is user language | keep (un-italicise *farm*) | 2 | Has a key (`vwp_days`: `docs/configuration.md:16`, `internal/env/env.go:37`) but it is a term herd managers say and set: `docs/configuration.md:41`, `internal/lists/builder.go:61`, `internal/lactation/breeding.go:70-73`. The entry itself carries no key. Headword "VWP" or "voluntary waiting period" are both acceptable so long as both forms are recorded. |
| 49 | withdrawal period | drift (universal claim) | rewrite. **Debatable** on shape: one entry that distinguishes milk withdrawal from meat withdrawal, or two entries (*milk withdrawal*, *meat withdrawal*) each naming the other. Keeping the text as it stands, or retiring it, is not acceptable. | 3 | "always withheld from the bulk tank ... never counted as saleable" is false for a meat withdrawal. See section 4, D1. |
| 51 | withhold sweep | mechanism vs guarantee | reframe. **Debatable**: either (a) reframe as an entry for the user-facing thing, e.g. *withhold list* carrying the guarantee "every cow with an open milk withdrawal is on it before the session opens", or (b) retire the entry and leave the guarantee in its existing homes (`README.md:20-22`, `docs/configuration.md:26-28`). Both acceptable. Keeping "withhold sweep" as a headword is not, and neither is retiring it with no mention of where the guarantee lives. | 1 | Named for an internal routine: `internal/treatment/withdrawal.go:89-92` (`sweepWithheld`, unexported). Users rely on the guarantee, not the pass. |

## 3. Tally

| Verdict | Count | Entries |
| --- | --- | --- |
| retire | 8 | Env, farm, GroupManager, HerdStore, late-reading rule, ListBuilder, MeterIngest, user |
| reframe | 1 | withhold sweep (or retire with the guarantee's home named; debatable) |
| merge | 1 | lactation number into parity |
| rename | 1 | days in lactation to days in milk |
| rewrite | 3 | dry period (trim), heifer (stub to real entry), withdrawal period (drift) |
| keep | 8 | cow, management group, parity as they are in substance; dry off, lactation, milking, session, VWP with light edits |
| **Total** | **22** | A good result leaves 12 entries (13 if withhold sweep is reframed as *withhold list*, one more if withdrawal is split in two), plus the gap entry *service*. |

## 4. Drift findings

- **D1. Universal claim against typed constants.** `docs/glossary.md:49` says a cow in a withdrawal period "is always withheld from the bulk tank, and her milk is never counted as saleable until the period has ended". The code splits withdrawal into two kinds, `internal/treatment/withdrawal.go:15-20` (`MilkWithdrawal WithdrawalKind = iota`, `MeatWithdrawal`), and only the milk kind withholds: `internal/treatment/withdrawal.go:100-102` skips every other kind when the withheld set is built. A meat withdrawal only marks the animal on the cull list: `internal/lists/builder.go:81-83`. Corroborated by `docs/decisions/0001-milk-and-meat-withdrawal-tracked-separately.md:26-28` and `docs/configuration.md:46-48`. The code and the decision are right; the glossary is wrong.
- **D2. Routine named in a user-facing doc.** `docs/configuration.md:29` says the withhold list "is rebuilt by the withhold sweep when a session opens". That is the internal routine `internal/treatment/withdrawal.go:92`; users need only the guarantee, which the same paragraph already states at `docs/configuration.md:27-28`. The clause naming the sweep should go.
- **D3. Headword drift.** `docs/glossary.md:11` "days in lactation" against "days in milk" in every source: `README.md:14`, `docs/configuration.md:23`, `internal/lactation/lactation.go:37`. Propagated inside the glossary at `docs/glossary.md:27`.
- **D4. Header.** `docs/glossary.md:4` "Gaps: none." against the undefined "service" (section 7).

Not drift (agrees): `docs/glossary.md:15` "defaults to 60" and "seven days" against `docs/configuration.md:14-15` and `internal/env/env.go:17`, `:24`; `docs/glossary.md:43` "two or three a day" against `docs/configuration.md:11`.

## 5. The bloated entry: dry period (`docs/glossary.md:15`)

155 words of definition. Kept: sentences 1 and 2 ("The span between a cow's *dry off* and her next calving, in which she is not milked. It is not the *dry off*, which is the event that starts it."). Cut:

| # | Cut sentence | Why cut | Home |
| --- | --- | --- | --- |
| 3 | "The target length is set by `dry_period_days`, which defaults to 60." | config key | `docs/configuration.md:14`; also `internal/env/env.go:17` and `:35` |
| 4 | "`LactationService` works out each cow's due dry-off date by counting the target length back from her expected calving date." | component name, mechanism | `docs/decisions/0003-dry-off-date-from-expected-calving.md:19-20`; also `docs/configuration.md:14`, `internal/lactation/breeding.go:64-68` |
| 5 | "*ListBuilder* puts her on the dry-off list seven days before that date." | component name, behaviour | `docs/configuration.md:15` and `:32-33`; also `internal/lists/builder.go:39-45` |
| 6 | "Because the expected calving date comes from her last service, a cow with no service on record never reaches the dry-off list and has to be dried off by hand." | a decision's consequence | `docs/decisions/0003-dry-off-date-from-expected-calving.md:20-21` and `:27-28`; partly `docs/configuration.md:33-35` |
| 7 | "A cow whose dry period will be shorter than 40 days is marked as short on the calving list." | behaviour | **Doc comment only:** `internal/lactation/lactation.go:15-17` (above `const ShortDryPeriodDays = 40`, line 18). Nowhere in the docs. `internal/lists/builder.go:49-50` mentions a "short dry period" marker but never says what counts as short: a false home. The calving list paragraph at `docs/configuration.md:37-39` does not mention the marker at all. |
| 8 | "The default was 56 days until release 2.3, when it was raised to 60 because cows calving a few days early kept falling inside the 54-day minimum of the dry cow tubes in use." | history | **Homeless:** stated nowhere else. `internal/env/env.go:15-16` says only "This default has history", without the history: a false home. `docs/decisions/0003-dry-off-date-from-expected-calving.md` is about how the date is computed and says nothing of the default. A correct run reports that cutting this sentence loses it unless it is given a home first (a decision record or a note in `docs/configuration.md`), and does not silently drop it. |

## 6. Outside edges

References outside the glossary that lean on a retired or reframed entry:

| Where | What | Action |
| --- | --- | --- |
| `internal/env/env.go:49` | `(glossary: Env)` | remove the citation; the entry is retired |
| `internal/treatment/withdrawal.go:90` | `(glossary: withhold sweep)` | remove the citation (or repoint to *withhold list* if reframed that way) |
| `docs/configuration.md:29` | names "the withhold sweep" | drop the clause (D2) |
| `docs/conventions.md:10-11` | "Every new exported type gets a glossary entry in the same pull request" | flag: this rule is what produced the component entries; it contradicts test 1 and should be removed or replaced |

Not edges:

- `internal/herd/animal.go:24` `(glossary: parity)`: *parity* is kept. Leave it.
- `docs/conventions.md:7-9`, "Identifiers take their words from the glossary": fine, that is the right direction of dependence.
- Ordinary uses of the code names as code (`docs/conventions.md:20` and `:33` `env.Env`, `cmd/byre/main.go:51-57`, `docs/decisions/0003-dry-off-date-from-expected-calving.md:19` `LactationService`) and ordinary prose uses of "farm" and "user" need no change: retiring a glossary entry does not rename the code or ban the word.

Edges inside the glossary (italic references to entries that go): *farm* at `docs/glossary.md:17` (goes with Env), `:43`, `:47`; *ListBuilder* at `:15` (cut) and `:27` (cut); *days in lactation* at `:27` (cut); *lactations* at `:29` (goes with the merge).

## 7. Gaps

- **Expected: service** (with the verb serve / served). The breeding event: one insemination of a cow or heifer, by AI or by the bull. Used throughout: `README.md:15`, `docs/configuration.md:13`, `:34`, `:38-39`, `:41-42`, `:62`, `docs/decisions/0003-dry-off-date-from-expected-calving.md:10`, `:21`, `:27`, `:29-32`, and inside the glossary itself at `docs/glossary.md:15` and `:47` ("not served"). Never defined. The type was deliberately named to dodge it: `internal/lactation/breeding.go:12-14` (`Insemination`), explained at `docs/conventions.md:12-14`: `Service` already means a long-lived component (`TreatmentService`, `LactationService`). The collision is live: `cmd/byre/main.go:66` and `:98` use "serve" in the HTTP sense while `internal/lists/builder.go:63` is the serve list. This is exactly the word a newcomer would misread, so it passes test 2. The new entry should define the word (and the verb) in the farm's sense and nothing more; the type name `Insemination` stays in the code and in `docs/conventions.md`.
- Acceptable extras (none required):
  - **calving**: used in most entries and at `README.md:14`; a careful reader may call it an ordinary word. Either answer is fine.
  - **withhold list**: `README.md:20`, `docs/configuration.md:26`; the natural home for the guarantee if withhold sweep is reframed.
  - **close-up**: `README.md:24`, `docs/configuration.md:17`, `internal/herd/group.go:16`; trade jargon a developer would not know.
  - **milk withdrawal / meat withdrawal**, if the run chose to split *withdrawal period*.
  - **dry cow**, **in-calf**, **maiden heifer**, **ear tag**: defensible but not expected.

## 8. Decoys

| # | Decoy | Where | Fooled verdict | Correct verdict |
| --- | --- | --- | --- | --- |
| 1 | `Session` struct shares its name with a kept word | `internal/milking/session.go:20-25` (also `Milking` at `:27-28`, `Lactation` at `internal/lactation/lactation.go:20-22`) | retire *session* (or *milking*, *lactation*) as "a type name", test 1 | keep: the struct is a bare day-and-slot key; the word is what milkers say |
| 2 | VWP has a config key | `docs/configuration.md:16`, `internal/env/env.go:37` | retire as configuration, or reframe | keep: users say and set it |
| 3 | `Env` is in nearly every file | 10 of 11 Go files; `docs/conventions.md:20` | keep because it is pervasive and developers "say" it | retire, test 1 |
| 4 | heifer is a redirect stub | `docs/glossary.md:23` | merge heifer into cow, or retire the stub | rewrite into a real entry; code and docs distinguish them |
| 5 | milking and session look like synonyms | `docs/glossary.md:39`, `:43` | merge | keep both, add the missing reciprocal pointer to *milking* |
| 6 | parity and lactation number can be argued distinct (calvings against lactations) | `docs/glossary.md:29`, `:41` | keep both as distinct | merge: same number here (`internal/lactation/lactation.go:71`, `:75`), and "lactation number" is used nowhere |
| 7 | management group beside GroupManager | `docs/glossary.md:21`, `:35` | retire both as code, or keep both as "the concept and its owner" | keep the concept, retire the component |
| 8 | late-reading rule sounds like domain language | `docs/glossary.md:31` | keep, or fold into *session* | retire: a decision restated, name used nowhere |
| 9 | withhold sweep carries a real guarantee | `docs/glossary.md:51` | keep as is, or retire and lose the guarantee | reframe (or retire naming the guarantee's home) |
| 10 | False home for the 40-day sentence | `internal/lists/builder.go:49-50` | cite it as a home, so the sentence looks safely documented twice | only home is `internal/lactation/lactation.go:15-17`, a doc comment; say so |
| 11 | False home for the history sentence | `internal/env/env.go:15-16` | claim the history is recorded in the code | homeless; flag before cutting |
| 12 | A citation of a kept term | `internal/herd/animal.go:24` | list it as an edge to fix | not an edge |
| 13 | The sound conventions line | `docs/conventions.md:7-9` | flag it along with the line below it | fine; only `docs/conventions.md:10-11` is flagged |
| 14 | `Gaps: none.` | `docs/glossary.md:4` | report no gaps | report *service* |
| 15 | Other constant blocks that do not contradict anything | `internal/herd/animal.go:10-13`, `internal/milking/session.go:14-18`, `internal/herd/group.go:13-17` | report drift against *session* or *management group* | none: the only contradicted claim is `docs/glossary.md:49` |
| 16 | farm and user are italicised or used widely | `docs/glossary.md:17`, `:43`, `:47`; `README.md:45` | keep because other entries depend on them | retire; un-italicise |

## 9. What the graders check

Deterministic `regex` graders carry the case. They grade only what a correct run must do whichever way the debatable items fall, and the file names say which planted rule each one checks.

On the written glossary (`docs/glossary.md`), by entry heading (`**term**` at the start of a line):

| Grader | Plant |
|---|---|
| `components-retired`, `no-code-names` | component names; `GroupManager` beside *management group*; `Insemination`, `LactationService`, `sweepWithheld` never admitted |
| `pervasive-identifier-retired` | `Env` |
| `ordinary-word-retired` | *user* |
| `decision-only-retired` | *late-reading rule* |
| `mechanism-name-retired` | *withhold sweep* (true under reframe and under retire) |
| `synonym-merged`, `synonym-recorded-not-used` | *lactation number* into *parity*, recorded as not used |
| `unused-headword-gone` | *days in lactation* (true under rename and under retire) |
| `concept-kept-management-group`, `sound-term-kept-cow` | the concept beside its component; a sound term |
| `distinction-milking-names-session`, `distinction-session-names-milking` | *milking* / *session*, made two-sided; the `Session` key type decoy |
| `redirect-rewritten-heifer` | the "See *cow*" stub becomes a real entry |
| `user-facing-term-kept` | *VWP*, under either form of the headword |
| `no-entry-over-80-words`, `bloated-entry-cut` | the bloated *dry period* entry: its history and its config key |
| `disputed-universal-not-asserted` | "always withheld from the bulk tank" no longer asserted, whether the entry is rewritten or split |
| `header-admission-replaced` | the header's admission rule |
| `gap-service-proposed` | *service* in the file's header, on its gaps line |

On the report (the last message): `drift-withdrawal-cited` (`withdrawal.go` at 13-20 or 100-102), `edge-withdrawal-cited` (`withdrawal.go` at 88-92), `edge-env-cited`, `edge-configuration-cited`, `edge-conventions-cited`, `homeless-history-sentence`. Citations match on the basename and the first line number, and tolerate backticks, `L9`, "lines 15-20" and comma lists.

One narrow `llm` grader, `forty-day-sentence-home`, reads the report: it fails a run that calls the doc-comment-only sentence homeless, or that homes it to `builder.go`, and passes anything else. The judge sees only the report, so a run that drops the sentence without accounting for it passes.

Not graded:

- *farm*. This key retires it as an ordinary word, but three entries lean on it and the key's own author called keeping it "mildly arguable". The owner has not ruled on it.
- The shape of *withdrawal period* (one entry or two), where the withhold guarantee lands, and whether *days in lactation* is renamed to *days in milk* or only surfaced.
- The label on light rewrites (*dry off*, *lactation*), extra gaps (*calving*, *withhold list*, *close-up*), and `animal.go:24` wrongly listed as an edge.
- *parity* against *lactation number* beyond the heading: a dairy specialist could argue they differ, though in this code they are the same count and the second word is used nowhere.

Known limits: `homeless-history-sentence` is a proximity match between a word for "no home" and the sentence, so an unusual heading can fail a correct run. Whether a run cites `env.go:15-16` as the sentence's home is not checked directly: a correct report may name that file while dismissing it.

## 10. Held out

This is the second held-out fixture, in a domain with nothing in common with the input the skill was first tuned on: Tessera, the first, is a tiling window manager like that input, so it catches fitting to that input's text but is weaker at catching fitting to its domain. Byre was built on 2026-09-19 by an agent that had not seen the `lexicon` skill, the other fixtures or their keys, working only from a list of defect kinds. This key is that agent's; every `file:line` the graders rely on was checked afterwards against the files.

It stays held out only while this holds: **look at its score, never edit the skill in response to a specific failure here.** Once a failure on Byre shapes the skill's wording, Byre becomes a regression fixture, and a new held-out fixture is needed. Fixing a grader or this key because it was wrong does not break the rule; changing the skill does.
