# Expected findings: Tessera lexicon

## 1. Header

- Fixture root: `fixture/`, beside this file. Every path below is relative to it.
- Lexicon: `docs/lexicon.md`, **22 entries** (lines 11 to 53, one entry per odd line).
- The three tests:
  1. **Language, not code**: a term is admitted for what people say about using or developing the system, not because a part of the code bears the name.
  2. **Needs defining**: without the entry someone would misunderstand or lack the word; ordinary words in their ordinary sense, and words whose only content is a decision, do not qualify.
  3. **One word per concept**: synonyms merge under the word actually used; distinct concepts stay distinct and each names the other.
- Entry shape: meaning and distinctions only; no mechanism, config keys, history or component names; about fifty words at most.
- What is wrong with the lexicon's header (`docs/lexicon.md:3-7`):
  - The admission sentence (`docs/lexicon.md:7`) is wrong: it admits anything "the team has given a name, whether in code, in a decision record or in conversation". That lets in class names (fails test 1) and decisions (fails test 2). It should admit only language people use about the system that needs defining.
  - The provenance line (`docs/lexicon.md:3`) records the sprawl mechanism: entries added "in the pull request that introduces a new class, command or config key". `docs/conventions.md:8` repeats the instruction.
  - `Gaps: none.` (`docs/lexicon.md:5`) is false: "stack" is used throughout and never defined (section 7).

## 2. Entries

| Line | Entry | Verdict | Test | Why, with evidence |
| --- | --- | --- | --- | --- |
| 11 | click-to-focus policy | retire | 2 (decision-only) | The whole content restates the decision of ADR 0002 (`docs/adr/0002-focus-does-not-follow-the-pointer.md:13`) plus its first consequence (`:17`). The name appears nowhere outside the lexicon. Users already get the behaviour at `docs/configuration.md:76`. |
| 13 | config file | retire | 2 (ordinary word) | Ordinary word in its ordinary sense. Continues to be used freely in prose (for example `README.md:11`, `docs/configuration.md:3`); that is not an edge. |
| 15 | context | retire | 1 (pervasive identifier) | Names the `WmContext` object and the `ctx` parameter (`src/Tessera/WmContext.cs:43`). It appears in 8 of the 11 source files, about 105 times, but nobody says it when talking about using Tessera or its behaviour. Its proper home already exists: `docs/conventions.md:15`. Frequency in code is not a reason to keep. |
| 17 | floating window | keep (light rewrite) | passes 1, 2, 3 | Real user term (`README.md:10`, `docs/configuration.md:97`). Drop the last sentence, which names the `WorkspaceManager` component. Once *unmanaged window* is a real entry, this one should name it. Labelling this "rewrite" is acceptable if the change is only that. |
| 19 | HotkeyListener | retire | 1 (component) | Class name (`src/Tessera/Input/HotkeyListener.cs:20`). Used nowhere in user talk. |
| 21 | layout | rewrite (trim) | entry shape | Correct, needed term; the definition is 158 words and carries behaviour, a config key, two component names, an ADR's consequences and a piece of history. Keep the first sentence (optionally the second). See section 5. |
| 23 | LayoutEngine | retire | 1 (component) | Class name (`src/Tessera/Layouts/LayoutEngine.cs:12`). Cited from a doc comment at `src/Tessera/Layouts/LayoutEngine.cs:9`: an edge. |
| 25 | main tile | keep | passes 1, 2, 3 | User term (`README.md:7`, `docs/configuration.md:50`, `:58`, `:68`). Its definition leans on "the stack", which is not italicized because there is no such entry: that is the gap. |
| 27 | move | keep (add the distinction) | 3 (distinction must survive) | Users must not conflate move and send (`docs/configuration.md:73-74`; `src/Tessera/Workspaces/WorkspaceManager.cs:70`, `:82`). The entry does not name *send*; it must. Merging move and send is wrong. |
| 29 | orphan sweep | reframe — **debatable** | 1 (mechanism, not the guarantee) | Named for an internal routine (`src/Tessera/Workspaces/WorkspaceManager.cs:97-100`). What users rely on is the guarantee that no window is stranded when a monitor goes away (`README.md:12`). Acceptable: (a) **reframe** as an entry for the guarantee (for example "stranded window" / "no stranded windows") without the routine's name; or (b) **retire**, stating explicitly that the guarantee survives in its existing home `README.md:12` and `docs/configuration.md:105`. Not acceptable: keep under the routine's name, or retire with no word about the guarantee. |
| 31 | pane | merge into *tile* | 3 (synonym) | Same concept as *tile* (`docs/lexicon.md:43`). "pane" appears nowhere in code or docs outside this entry; "tile" is used everywhere. Merge into *tile*, recording "pane" as not used. |
| 33 | rule | rewrite (drift) | passes; claim is false | Term is sound. The claim "applied only once ... nothing ... ever triggers a rule again" is contradicted by the `RuleTrigger` enum (`src/Tessera/Rules/Rule.cs:4-11`, `TitleChange` at `:10`) and `src/Tessera/Rules/RuleEngine.cs:37`. ADR 0003 corroborates the code (`docs/adr/0003-rules-reapplied-on-title-change.md:13`). Fix the lexicon, not the code. See section 4. |
| 35 | RuleEngine | retire | 1 (component) | Class name (`src/Tessera/Rules/RuleEngine.cs:13`). |
| 37 | send | keep | 3 (distinction must survive) | Already names *move*. See *move*. |
| 39 | shortcut | retire, or keep with the sense stated | 2 | Accepted either way, by the owner's ruling of 2026-09-20 (THE-212, won't fix). The entry is an ordinary word in its ordinary sense, and the builder's key retires it. Every run keeps it and adds "Not a Windows shortcut file". The owner's reading: the documentation uses a bare word that can be read another way (`[shortcuts]`, "## Shortcuts and commands"), so a run that keeps the entry and says which sense is meant is doing its job, and the ambiguity is the documentation's. Not graded. Only other lexicon reference is from *HotkeyListener* (`docs/lexicon.md:19`), itself retired. |
| 41 | split ratio | keep | passes 1, 2, 3 | Looks technical because it has a key (`split_ratio`, `docs/configuration.md:50`) and a property (`src/Tessera/Config/TesseraConfig.cs:28`), but users say it and set it (`README.md:9`, `docs/configuration.md:56`, `:69`). The entry itself carries no key. The citation at `src/Tessera/Layouts/MainStackLayout.cs:9` is valid. |
| 43 | tile | keep (merge target) | 3 | The word in use. Absorbs *pane*; add "pane: not used". |
| 45 | unmanaged window | rewrite into a real entry — NOT merge | 3 (distinct concept) | The stub redirects to *floating window*, but the two are distinct: a floating window is managed and belongs to a workspace; an unmanaged window belongs to none and no command touches it. Docs: `docs/configuration.md:93-99`, `docs/adr/0003-rules-reapplied-on-title-change.md:19`. Code: `RuleAction.Float` vs `RuleAction.Ignore` (`src/Tessera/Rules/Rule.cs:19-23`), `src/Tessera/WmContext.cs:73-77`, `src/Tessera/Workspaces/WorkspaceManager.cs:41-43` vs `:48-49`. Each entry should name the other. |
| 47 | work area | keep | passes 1, 2, 3 | Used throughout in a precise sense that "screen" or "monitor" would get wrong (`README.md:7`, `docs/configuration.md:50`, `:52`). It is also the platform's word, used here in the same sense; keeping it is the expected answer. |
| 49 | workspace | keep | 1 (concept of a concept/component pair) | The domain concept (`README.md:8`, `docs/configuration.md:101-103`). That a `Workspace` class exists (`src/Tessera/Workspaces/Workspace.cs:43`) neither earns nor costs it the entry. |
| 51 | WorkspaceManager | retire | 1 (component of the pair) | The class that realizes workspaces (`src/Tessera/Workspaces/WorkspaceManager.cs:9`). Keep the concept, retire the component. Also named inside *floating window* (`docs/lexicon.md:17`). |
| 53 | zoom | rename to *promote* | 3 (headword drift) | No source uses "zoom". Code and every doc say promote: `README.md:9`, `docs/configuration.md:18`, `:58`, `:68`, `src/Tessera/Input/HotkeyListener.cs:83-84`, `src/Tessera/Workspaces/Workspace.cs:107-110`. The definition is fine; the headword is wrong. |

## 3. Tally

| Verdict | Count | Entries |
| --- | --- | --- |
| retire | 7, or 8 with *shortcut* (accepted either way) | click-to-focus policy, config file, context, HotkeyListener, LayoutEngine, RuleEngine, WorkspaceManager |
| reframe | 1 | orphan sweep (retire-with-guarantee-kept also acceptable: then retire 9, reframe 0) |
| merge | 1 | pane → tile |
| rename | 1 | zoom → promote |
| rewrite | 3 | layout (trim), rule (drift), unmanaged window (stub → real entry) |
| keep | 8 | floating window (drop component sentence), main tile, move (name *send*), send, split ratio, tile (absorbs pane), work area, workspace |
| **Total** | **22** | |

After the work the lexicon has 12 or 13 entries (13 if the guarantee gets its own entry), plus 1 if the gap "stack" is filled.

## 4. Drift findings

1. **Universal claim vs enum.** `docs/lexicon.md:33` says a rule "is applied only once, when the window first opens; nothing that happens to the window afterwards ever triggers a rule again". Code: `src/Tessera/Rules/Rule.cs:4-11` splits rules by `RuleTrigger` into `Open` (`:7`) and `TitleChange` (`:10`); `src/Tessera/Rules/RuleEngine.cs:33-37` re-applies `TitleChange` rules on every title change; `src/Tessera/Config/TesseraConfig.cs:112` reads the trigger. Corroboration: `docs/adr/0003-rules-reapplied-on-title-change.md:13`, `docs/configuration.md:87`, sample at `docs/configuration.md:37`. The lexicon is the side that is wrong.
2. **Headword no source uses.** `docs/lexicon.md:53` "zoom" vs "promote" at `docs/configuration.md:68`, `README.md:9`, `src/Tessera/Input/HotkeyListener.cs:83`, `src/Tessera/Workspaces/Workspace.cs:110`.
3. **Mechanism name in a user document.** `docs/configuration.md:105` names "the orphan sweep"; users need only the guarantee, which `README.md:12` states without the name. The routine's name belongs in code (`src/Tessera/Workspaces/WorkspaceManager.cs:97`, `:100`), where it may stay.
4. **Stub hides a distinction.** `docs/lexicon.md:45` ("See *floating window*") vs `docs/configuration.md:95` ("`float` and `ignore` are not the same thing") and `src/Tessera/Rules/Rule.cs:19-23`.
5. **One-sided distinction.** `docs/lexicon.md:37` (*send*) names *move*; `docs/lexicon.md:27` (*move*) does not name *send*.
6. **Header.** `docs/lexicon.md:5` "Gaps: none." vs the undefined "stack" (section 7); `docs/lexicon.md:7` admission sentence vs the three tests.

## 5. The bloated entry: *layout* (`docs/lexicon.md:21`)

158 words of definition (160 counting the headword and dash). Sentences in order:

| # | Sentence (start) | Keep or cut | Home |
| --- | --- | --- | --- |
| 1 | "The scheme by which a *workspace*'s tiled windows get their *tiles*: main-stack or columns." | keep | — |
| 2 | "A *workspace* has one layout at a time, which the user can cycle." | keep (cutting the cycling clause is fine; home `docs/configuration.md:56`, `:70`) | — |
| 3 | "Main-stack puts one window in the *main tile* ... columns gives every window an equal column." | cut (behaviour) | `docs/configuration.md:56`; also `README.md:7`, `src/Tessera/Layouts/MainStackLayout.cs:7-8`, `src/Tessera/Layouts/ColumnsLayout.cs:7-8` |
| 4 | "New workspaces start in the layout named by the `default_layout` key." | cut (config key) | `docs/configuration.md:56`, `docs/configuration.md:49`; `src/Tessera/Config/TesseraConfig.cs:23` |
| 5 | "The `LayoutEngine` asks the layout for rectangles and hands them to the `WindowMover` ... single batch." | cut (components, mechanism) | `docs/adr/0001-layouts-are-pure-functions.md:13`; `src/Tessera/Layouts/LayoutEngine.cs:9-10` |
| 6 | "When a *workspace* holds a single window, every layout gives it the whole *work area*." | cut (behaviour) | **Doc comment only**: `src/Tessera/Layouts/ILayout.cs:38-39`, nowhere else. |
| 7 | "Because a layout is a pure function ... dragging the edge of a tiled window has no lasting effect." | cut (ADR consequence) | `docs/adr/0001-layouts-are-pure-functions.md:20` (decision at `:13`) |
| 8 | "The default was columns until 0.4; it became main-stack because on ultrawide monitors equal columns pushed the editor off-centre." | cut (history) | **Homeless**: stated nowhere else. It must not be silently dropped: report it and propose a home (a note in an ADR or beside `default_layout` in `docs/configuration.md`). |

Call-outs:

- **Doc-comment-only sentence (6).** Its only statement is `src/Tessera/Layouts/ILayout.cs:38-39`. `src/Tessera/Workspaces/Workspace.cs:70-71` mentions "the single-window case, which the layouts treat specially" without saying what happens: a false home. `src/Tessera/Layouts/MainStackLayout.cs:22-23` implements the behaviour but states nothing. A run should note that a user-visible behaviour is documented only in a doc comment.
- **Homeless sentence (8).** `src/Tessera/Config/TesseraConfig.cs:24` says "This default has history; ask before changing it." without giving the history: a false home. `docs/configuration.md:49` gives the default with no history. Grep for `0.4`, `ultrawide`, `off-centre` finds only `docs/lexicon.md:21`.

## 6. Outside edges

References outside the lexicon to a term that is retired (or whose name goes):

| Where | What | Action |
| --- | --- | --- |
| `src/Tessera/Layouts/LayoutEngine.cs:9` | `(lexicon: LayoutEngine)` | Remove the citation. |
| `src/Tessera/WmContext.cs:39` | `(lexicon: context)` | Remove the citation. |
| `docs/configuration.md:105` | "the orphan sweep" named in a user document | Reword to state the guarantee only. |
| `docs/conventions.md:8` | "When a pull request adds a class, add a lexicon entry for the class" | Flag: this instruction is what produced the component entries; it contradicts test 1. |
| `docs/lexicon.md:17` | *floating window* names `WorkspaceManager` | Inside the lexicon; handled by the light rewrite. |
| `docs/lexicon.md:19` | *HotkeyListener* italicizes *shortcuts* | Inside the lexicon; both retired, nothing to do. |

Not edges:

- `src/Tessera/Layouts/MainStackLayout.cs:9` `(lexicon: split ratio)`: the term is kept; the citation stays.
- `docs/conventions.md:7` ("Take identifiers from the lexicon"): fine, and stays.
- Code identifiers and code-facing mentions of component names are code names being used as code names, not lexicon references: `LayoutEngine` and `WindowMover` in `docs/adr/0001-layouts-are-pure-functions.md:13`; `WmContext ctx` in `docs/conventions.md:15-17`; "The orphan sweep" and `SweepOrphans` in `src/Tessera/Workspaces/WorkspaceManager.cs:97-100`. They stay.
- "config file" and "shortcut" in ordinary prose (README, configuration, doc comments) stay: retiring an ordinary word's entry does not retire the word.
- "click-to-focus policy", "pane" and "zoom" have no outside references at all.

## 7. Gaps

- **Expected: "stack"**: the tiles of the main-stack layout other than the main tile. Used throughout: `README.md:7`, `README.md:9`, `docs/configuration.md:58`, `docs/configuration.md:66`, `docs/adr/0001-layouts-are-pure-functions.md:21`, `src/Tessera/Workspaces/Workspace.cs:75`, `src/Tessera/Layouts/MainStackLayout.cs:8`, `:38`, and inside the lexicon's own *main tile* entry (`docs/lexicon.md:25`, un-italicized). Never defined. The code deliberately dodges the word: the class is `SecondaryArea` (`src/Tessera/Layouts/MainStackLayout.cs:42`, comment at `:38-40`) because `Stack` collides with `System.Collections.Generic.Stack<T>` and the call stack, as `docs/conventions.md:9` says. The absence of a `Stack` class is not evidence that the word is unused; `SecondaryArea` must NOT be proposed as the lexicon term.
- Acceptable extras (not required, not penalized): "gutter" (`docs/configuration.md:52`), "in view" as said of a workspace (`docs/configuration.md:72`, `src/Tessera/Workspaces/Workspace.cs:60-61`), "managed window" as the counterpart of unmanaged, and the no-stranded-windows guarantee if *orphan sweep* was retired rather than reframed. "monitor", "focus" and "swap" are ordinary here and need no entry; proposing them is mildly wrong but not a failure.

## 8. Decoys

| Decoy | Where | Fooled verdict | Correct verdict |
| --- | --- | --- | --- |
| `Rule` is a class | `src/Tessera/Rules/Rule.cs:30` (a record that "holds values only", `:27`) | Retire *rule* as a code name (test 1) | Keep *rule*: users write rules and say the word (`README.md:11`, `docs/configuration.md:78-80`); the record is a narrow holder. Only the drift needs fixing. |
| `Workspace` is a class | `src/Tessera/Workspaces/Workspace.cs:43` | Retire *workspace* together with *WorkspaceManager* | Keep the concept, retire the component. |
| *split ratio* has a config key and a property | `docs/configuration.md:50`, `src/Tessera/Config/TesseraConfig.cs:28-29` | Retire as a config key / technical setting | Keep: users say it and set it. |
| *context* is everywhere in code | 8 of 11 source files; `docs/conventions.md:15` | Keep because it is pervasive | Retire: nobody says it about using the system. |
| Valid citation | `src/Tessera/Layouts/MainStackLayout.cs:9` `(lexicon: split ratio)` | Listed as an edge to fix | Not an edge. |
| Redirect stub | `docs/lexicon.md:45` | Merge *unmanaged window* into *floating window* | Rewrite into a real, distinct entry. |
| Near-synonym verbs | `docs/lexicon.md:27`, `:37` | Merge *move* and *send* | Keep both; each names the other. |
| True synonyms | `docs/lexicon.md:31`, `:43` | Keep both *pane* and *tile*, or merge into *pane* | Merge into *tile*; "pane" is used nowhere. |
| False home for the single-window sentence | `src/Tessera/Workspaces/Workspace.cs:70-71` | Cite it as the sentence's home (or as a second home) | It mentions the topic without stating it; the only home is `src/Tessera/Layouts/ILayout.cs:38-39`. |
| False home for the history sentence | `src/Tessera/Config/TesseraConfig.cs:24` | Cite it as the home and cut the sentence silently | The sentence is homeless; say so. |
| Mechanism entry with a user-facing guarantee | `docs/lexicon.md:29`, `docs/configuration.md:105` | Keep *orphan sweep* because a user document uses it, or retire it and lose the guarantee | The name goes (and the user document's mention is drift); the guarantee survives. |
| Policy-sounding name | `docs/lexicon.md:11` | Keep as a domain rule users rely on | Retire: decision-only, name used nowhere; ADR 0002 is its home. |
| "Gaps: none." | `docs/lexicon.md:5` | Report no gaps | "stack" is a gap. |
| `SecondaryArea` | `src/Tessera/Layouts/MainStackLayout.cs:42` | Conclude "stack" is not the project's word, or propose "secondary area" | "stack" is the word; the class name is a deliberate dodge (`docs/conventions.md:9`). |
| Conventions line | `docs/conventions.md:8` | Treat as authority for keeping class entries | Flag it as the source of sprawl. |

## 9. What the graders check

Deterministic `regex` graders carry the case. They grade only what a correct run must do whichever way the debatable items fall, and the file names say which planted rule each one checks.

On the written lexicon (`docs/lexicon.md`), by entry heading (`**term**` at the start of a line):

| Grader | Plant |
|---|---|
| `components-retired`, `no-code-names` | component names; `WorkspaceManager` beside *workspace*; `SecondaryArea`, `WmContext`, `ctx` never admitted |
| `pervasive-identifier-retired` | *context* |
| `ordinary-words-retired` | *config file*. *shortcut* is no longer graded: see its row |
| `decision-only-retired` | *click-to-focus policy* |
| `mechanism-name-retired` | *orphan sweep* (true under reframe and under retire) |
| `synonym-merged`, `synonym-recorded-not-used` | *pane* into *tile*, recorded as not used |
| `unused-headword-gone` | *zoom* (true under rename and under retire) |
| `concept-kept-workspace`, `concept-kept-rule` | the `Workspace` and `Rule` class decoys |
| `distinction-move-names-send`, `distinction-send-names-move` | *move* / *send*, made two-sided |
| `redirect-rewritten-unmanaged-window` | the "See *floating window*" stub becomes a real entry |
| `user-facing-term-kept` | *split ratio* |
| `domain-term-kept-work-area` | *work area* (owner's ruling, below) |
| `no-entry-over-80-words`, `history-cut-from-entry` | the bloated *layout* entry |
| `disputed-universal-not-asserted` | "applied only once ... ever" no longer asserted |
| `header-admission-replaced` | the header's admission rule |
| `gap-stack-proposed` | *stack* in the file's header, on its gaps line |

On the report (the last message): `drift-rule-cited` (`Rule.cs` at 3-11 or `RuleEngine.cs` at 33-37), `edge-layout-engine-cited`, `edge-wmcontext-cited`, `edge-configuration-cited`, `edge-conventions-cited`, `homeless-history-sentence`. Citations match on the basename and the first line number, and tolerate backticks, `L9`, "lines 4-11" and comma lists.

One narrow `llm` grader, `single-window-sentence-home`, reads the report: it fails a run that calls the doc-comment-only sentence homeless, or that homes it to `Workspace.cs`, and passes anything else. The judge sees only the report, so a run that drops the sentence without accounting for it passes.

Not graded: whether *zoom* is renamed to *promote* or only surfaced; where the no-stranded-windows guarantee lands; *floating window* naming *unmanaged window*; the label on light rewrites; extra gaps; `MainStackLayout.cs:9` wrongly listed as an edge.

Owner's ruling (2026-09-19) on *work area*: keep, and graded. It is also the Windows platform's word in the same sense, but the domain is tiling window managers, not the platform Tessera happens to run on. The word is not everyday English, its boundary is fixed by the system (the monitor minus the taskbar and docked toolbars), and it marks the distinction from the full screen that tiling depends on. Retiring it under test 2 is a failure.

Known limits: `homeless-history-sentence` is a proximity match between a word for "no home" and the sentence, so an unusual heading can fail a correct run. Whether a run cites `TesseraConfig.cs:24` as the sentence's home is not checked directly: a correct report may name that file while dismissing it.

## 10. Held out

This fixture exists so that there is always one input no iteration of the skill was tuned on. It was built on 2026-09-19 by an agent that had not seen the `lexicon` skill, the other fixtures or their keys, working only from a list of defect kinds. This key is that agent's; every `file:line` the graders rely on was checked afterwards against the files.

It stays held out only while this holds: **look at its score, never edit the skill in response to a specific failure here.** Once a failure on Tessera shapes the skill's wording, Tessera becomes a regression fixture like Shelfwise and Stockroom, and a new held-out fixture is needed. Fixing a grader or this key because it was wrong does not break the rule; changing the skill does.

Its domain is close to the one the skill was first tuned on (a tiling window manager), by the owner's choice. It tests a lexicon and code the skill has never met, not a domain it has never met.
