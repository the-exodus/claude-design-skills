# Answer key — Shelfwise lexicon consolidation fixture

Fixture root: `fixture/` beside this file (paths below are relative to it). The scaffold script copies it into the run's workspace; this file is never copied.
Lexicon: `docs/design/lexicon.md`, 31 entries, lines 10–70.

Tests: **1** language-not-code (a term is admitted for what people say about using or developing the system, not because a part of the code bears the name); **2** needs-defining (would someone talking about the system otherwise misunderstand or lack the word?); **3** one-word-per-concept (synonyms merge; distinct concepts stay distinct and name each other).

## Header

- Admission sentence (line 6) "…or a decision defined it" is wrong: a decision defines a rule, not a word. A correct run rewrites it to admit only words someone needs defined to talk about using or developing the system (and states that entries give meaning and distinctions, not mechanism).
- `Gaps: none.` (line 4) is wrong: at least *branch* (see Gaps).
- Provenance line: keep; a run may append a consolidation note.

## Per-entry verdicts

| Line | Entry | Verdict | Test | Why |
|---|---|---|---|---|
| 10 | book | retire | 2 | Ordinary word. The distinctions that matter are *title* vs *item*; "book" is one `format` value (`src/catalog/title.ts:6`). Cut content (DVDs/audiobooks) is visible in the code; nothing of meaning lost. |
| 12 | borrower | merge → patron | 3 | Synonym. The word appears nowhere in code or docs; *patron* is used everywhere. (Debatable only if the owner wants a "patron with a current loan" role — nothing in code or docs makes that distinction.) |
| 14 | catalog | rewrite (keep) — **debatable keep vs retire** | 2 | Domain word users meet ("search the catalog", README:4). Drop "Searched through the CatalogIndex" (component reference, test 1). A run retiring it as ordinary is defensible; not a failure either way. |
| 16 | CatalogIndex | retire | 1 | Component name (`src/catalog/catalog-index.ts:8`). Content lives in its doc comment (lines 4–7). |
| 18 | charge sweep | reframe → the guarantee "a returned item is never still charged" | 1 | Names a routine; its purpose is a guarantee users rely on (`docs/api.md:20–21`). The guarantee survives — as its own entry or folded into *return* / *fine* (**where it lands is debatable**); the routine name retires. Mechanism lives in ADR-0001 and `src/loans/loan-reconciler.ts:1–7`. Also a drift/outside edge: `docs/configuration.md:32` exposes the routine name to users. |
| 20 | date | retire | 2 | Ordinary word. The storage-format sentence has a home: `docs/conventions.md:10`. |
| 22 | due date | keep (optionally trim the config key → `docs/configuration.md:10`) | 2 | Meaningful domain term; related to renew/extend. |
| 24 | due slip | rewrite, headword → *receipt* — **surface as drift, do not settle silently** | 3 | Code and docs say receipt: `src/receipts/receipt.ts:8`, `docs/api.md:31–34`, `docs/adr/0005-keep-receipts.md:16`. ADR-0005:11 shows "due slip" was the retired paper artifact. Expected: propose the rename with evidence and leave the decision to the owner (or record the owner's choice). |
| 26 | extend | keep, rewrite to name *renew* | 3 | Distinction pair. Must say it adds days without restarting the loan period and does not count as a renewal (evidence `src/loans/renewal.ts:4–7`, `docs/api.md:16–18`, ADR-0004). Config key cut → `docs/configuration.md:13`. |
| 28 | fine | keep (config key may move to configuration.md) | 2 | Domain term. |
| 30 | FineCalculator | retire | 1 | Component (`src/loans/fines.ts:16`). Schedule order lives in ADR-0001 Consequences. |
| 32 | grace period | **keep** (decoy) | 2 | Looks technical because of the config key, but is a user-facing term: administrators set it, patrons experience it (`docs/configuration.md:11`). Trimming the key is optional. |
| 34 | hold | keep, rewrite | 1 | The domain concept stays. Cut "HoldManager allocates each returned item to the oldest waiting hold" — mechanism; home ADR-0003 (Decision) and `src/holds/hold-manager.ts:2–3, 26–27`. Should distinguish hold (on a title) from item. |
| 36 | hold queue | keep (may drop the ADR citation) | 2 | Domain term. |
| 38 | HoldManager | retire (decoy pair with *hold*) | 1 | Component (`src/holds/hold-manager.ts:12`). A type named after a domain concept does not make the concept code, nor the class a term. Outside edge `src/holds/hold-manager.ts:3`. |
| 40 | item | keep | 2/3 | Title vs item distinction. |
| 42 | library card | keep | 2 | Needed to define *member*. |
| 44 | loan | keep, rewrite | 1 | Drop "Persisted through the LoanRepository" (component). |
| 46 | LoanReconciler | retire | 1 | Component (`src/loans/loan-reconciler.ts:13`). |
| 48 | member | rewrite (NOT merge) | 3 | Redirect stub hides a distinct concept: a patron whose library card is active; only members may borrow or place holds. Evidence `src/patrons/patron.ts:14–20`, `docs/api.md:3–5`. Should name *patron* as the thing it is distinct from. Merging into patron is a failure. |
| 50 | NotificationQueue | retire | 1 | Component (`src/notifications/notification-queue.ts:11`). |
| 52 | overdue | keep, rewrite — **drift** | 2 | Second sentence ("always accrues a fine until returned") contradicted by code and ADR-0002. See Drift 1. |
| 54 | patron | keep (absorbs *borrower*) | 3 | |
| 56 | patron-first policy | retire | 1/2 | Decision-only: the whole entry restates ADR-0004's decision; the phrase occurs nowhere in code or docs. Home: `docs/adr/0004-holds-take-precedence-over-renewals.md` (Decision), `src/loans/renewal.ts:22`. (A run may add "cannot be renewed while the title has a waiting hold" as a distinction note under *renew* — acceptable, **debatable**.) |
| 58 | pickup window | keep, rewrite (bloated, ~140 words) | 2 | See "Bloated entry" below. |
| 60 | renew | keep, rewrite (decoy: `Renewal` DTO) | 2/3 | Keep the distinction from *extend* (it already names it). Cut the config key (→ `docs/configuration.md:12`) and "Implemented by `renew()`, which returns a `Renewal`" (code reference). |
| 62 | repository layer | retire | 1 | Component. Outside edge `docs/conventions.md:9`. |
| 64 | request context (ctx) | retire (decoy) | 1 | Ubiquitous identifier, but nobody uses the word to talk about using the system or its behaviour. Content home: `src/http/context.ts:4–7`, `docs/conventions.md:8`. |
| 66 | return | keep — **debatable keep vs retire** | 2 | Borderline ordinary word; a natural host for the charge-sweep guarantee. |
| 68 | title | keep | 3 | Title vs item. |
| 70 | waive | keep | 2 | Consistent with `OverdueState.Waived`; may be referenced from the rewritten *overdue*. |

Tally: retire 10 (book, date, CatalogIndex, FineCalculator, HoldManager, LoanReconciler, NotificationQueue, repository layer, request context, patron-first policy); reframe 1 (charge sweep → guarantee; the routine name retires); merge 1 (borrower → patron); the other 19 are kept, most with rewrites (due slip rename subject to owner decision).

## Drift findings (must be surfaced with evidence, not silently settled)

1. **overdue always accrues** — lexicon line 52 says "An overdue loan always accrues a fine until the item is returned." Code splits overdue into three states:
   - `src/loans/fines.ts:6–13` — `enum OverdueState { Accruing, Capped, Waived }`
   - `src/loans/fines.ts:26` — `accrueOneDay` returns early unless `Accruing`
   - `src/loans/fines.ts:28` — loan moves to `Capped` at `fines.capCents`
   - `src/loans/fines.ts:43` — `waive` sets `Waived`
   - corroborated by `docs/adr/0002-cap-overdue-fines.md:24–25`.
2. **due slip vs receipt** — lexicon line 24 headword vs `src/receipts/receipt.ts:8`, `src/receipts/receipt.ts:2`, `docs/api.md:31–34`, `docs/adr/0005-keep-receipts.md:16` (and ADR-0005:11 using "due slip" for the old printed paper).
3. **routine name in a user doc** — `docs/configuration.md:32` "When the nightly charge sweep runs": the user reference names the mechanism where users care about the guarantee (`docs/api.md:20`). Surface; propose rewording.

Bonus, unplanned but real (credit, not required): `src/loans/loan-reconciler.ts:17` only looks back 24 hours, while ADR-0001:11–13 says offline returns can sync "a day or more later" — the guarantee in `docs/api.md:20–21` may not hold for very late syncs, depending on whether `returnedSince` filters on recorded return time. **Debatable**; do not penalize either way.

## Bloated entry — pickup window (line 58)

Kept core: the period a patron has to collect an item held for them at their pickup branch (after which the hold lapses).

Cut sentences and their homes:

| Cut sentence | Home |
|---|---|
| Length set by `holds.pickupWindowDays` (default 7) | `docs/configuration.md:26`; ADR-0003:18–19; `src/config.ts:18,26` |
| **Window starts at check-in at the pickup branch, not when notified** | **ONLY a doc comment: `src/holds/hold-manager.ts:26–29`** (the code sets `readyAt` at line 33). Calling this homeless is a failure. |
| HoldManager marks ready; NotificationQueue notifies at once and reminds the day before close | ADR-0003:19–20; `src/notifications/notification-queue.ts:4–5` |
| Lapse → item to next hold; patron keeps no place | ADR-0003:20–22; `src/holds/hold-manager.ts:38`; `docs/api.md:28–29` (lapse only) |
| **"The window was shortened from ten days to seven after the 2023 pilot, when uncollected holds tied up popular titles for weeks."** | **HOMELESS — nowhere else.** Must be listed as having no home. |
| Staff cannot lengthen an individual window; missing it means a new hold | ADR-0003 Consequences (lines 26–28) |

## Outside edges (references to retired terms outside the lexicon)

- `src/loans/loan-reconciler.ts:2` — `(lexicon: charge sweep)`
- `src/holds/hold-manager.ts:3` — `(lexicon: HoldManager)`
- `docs/configuration.md:32` — "charge sweep" in a user reference
- `docs/conventions.md:9` — "repository layer"
- `docs/adr/0005-keep-receipts.md:11` — "due slip" (only if the rename is adopted; it is historical context in an ADR and should be left as is — ADRs are not edited)
- Not an outside edge to a retired term: `src/loans/renewal.ts:2` `(lexicon: renew)` — *renew* is kept. Listing it as needing change is a (minor) error.
- Also worth noting: `docs/conventions.md:3–4` claims identifiers take names from the lexicon — consistent with the owner's intent; no change needed.

## Gaps

- **branch** (expected) — a library location where items are shelved, lent, returned and holds collected. Used by users and docs throughout (`README.md:3–4`, `docs/api.md:21, 26, 29`, `src/holds/hold.ts:3`), never defined. The code dodges the word with `BranchSite` (`src/branches/branch-site.ts:5–8`, `docs/conventions.md:5–7`) because "branch" collides with git branches — exactly why the domain sense needs defining. *pickup branch* / *home branch* are covered by or may be sub-bullets of it.
- Optional, **debatable**: *checkout*, *extension*/*renewal* as noun forms, *lapse* (hold state). Proposing these is not an error; proposing component names (e.g. `BranchSite`, `OverdueState`) as gaps is.

## Decoys (what a fooled run would do)

| Decoy | Location | Fooled verdict | Correct |
|---|---|---|---|
| `HoldManager` class named after a domain concept | `src/holds/hold-manager.ts:12` | Retire *hold* along with HoldManager, or keep HoldManager because "hold" is domain | Keep *hold*, retire *HoldManager* |
| `Renewal` interface (API response DTO) | `src/loans/renewal.ts:13–19` | Retire *renew* as "a code name" | Keep *renew* |
| Doc comment that mentions the pickup-window notices without stating when the window starts | `src/notifications/notification-queue.ts:4–5` | Cite it as a home of "window starts at check-in" | Home is only `src/holds/hold-manager.ts:26–29` |
| Doc comment that mentions the pickup-window default "has history" without stating it | `src/config.ts:14–17` | Cite it as home for the ten→seven pilot sentence, so fail to list it homeless | The pilot sentence is homeless |
| `ctx` / `RequestContext` used in almost every file | `src/http/context.ts:8`, every handler | Keep *request context* because it is everywhere | Retire (test 1) |
| *grace period* has a config key | `docs/configuration.md:11` | Retire as a config/implementation detail | Keep (user-facing) |
| *member* stub "See *patron*" | lexicon line 48 | Merge into patron / delete as redirect | Rewrite as distinct concept |

## Judge amendments (round 3) — supersede the rows above where they conflict

- fine, waive, hold queue, library card, catalog: retiring under test 2 (ordinary library sense; specifics are decisions/config) is CORRECT by the owner's intent ("only words that NEED to be defined"); keeping them is acceptable but weaker. Do not penalise retirement.
- borrower: merge into patron (recorded as not used) remains the expected verdict; retiring it without the "not used" note is a miss.
- Overloads against programming-language senses (return value, a `title` string field) are noise — penalise.
- conventions.md:3-4 flagged as feeding sprawl: acceptable, not an error.

## Judge amendment (round 4) — recommended by the judge, first written down here

- charge sweep: reframe OR retire is correct, provided the guarantee keeps a home (`docs/api.md:20–21`). Retiring the routine's name is the part that must happen.
- return: keep vs retire is debatable; do not penalise either.

## What the graders check

Deterministic `regex` graders carry the case. They grade only what a correct run must do whichever way the debatable items fall, and the file names say which planted rule each one checks.

On the written lexicon (`docs/design/lexicon.md`), by entry heading (`**term**` at the start of a line):

| Grader | Plant |
|---|---|
| `components-retired`, `no-code-names` | component names; `HoldManager` beside *hold*; `BranchSite`, `OverdueState` never admitted |
| `pervasive-identifier-retired` | *request context*: everywhere in the code, not language |
| `ordinary-words-retired` | *book*, *date* |
| `decision-only-retired` | *patron-first policy* |
| `mechanism-name-retired` | *charge sweep* (true under reframe and under retire) |
| `synonym-merged`, `synonym-recorded-not-used` | *borrower* into *patron*, recorded as not used |
| `concept-kept-hold` | *hold* survives `HoldManager` |
| `distinction-renew-names-extend`, `distinction-extend-names-renew` | *renew* / *extend*, and the `Renewal` DTO decoy |
| `redirect-rewritten-member` | the "See *patron*" stub becomes a real entry |
| `user-facing-term-kept` | *grace period* |
| `no-entry-over-80-words`, `history-cut-from-entry` | the bloated *pickup window* entry |
| `disputed-universal-not-asserted` | "always accrues" no longer asserted |
| `header-admission-replaced` | the header's admission rule |
| `gap-branch-proposed` | *branch* on the file's Gaps line |

On the report (the last message): `drift-overdue-cited` (`fines.ts` at 5–13, 26, 28 or 43), `drift-receipt-cited`, `edge-hold-manager-cited`, `edge-loan-reconciler-cited`, `edge-configuration-cited`, `homeless-pilot-sentence`. Citations match on the basename and the first line number, and tolerate backticks, `L9`, "lines 6–13" and comma lists.

One narrow `llm` grader, `checkin-sentence-home`, reads the report: it fails a run that calls the doc-comment-only sentence homeless, or that homes it to `notification-queue.ts`, and passes anything else. A pattern cannot tell those apart. The judge sees only the report, so a run that drops the sentence without accounting for it passes; every run so far has kept it in the entry as meaning.

Not graded, because the key or the amendments accept more than one answer: catalog, fine, waive, hold queue, library card, return, due date; whether *due slip* is renamed or only surfaced; where the charge-sweep guarantee lands; `docs/conventions.md:9` as an outside edge; unplanned drift (credit, never required).

Known limits: `homeless-pilot-sentence` is a proximity match between a word for "no home" and the sentence, so a report that lists it under a differently worded heading fails. Whether a run cites `src/config.ts:14–17` as the sentence's home (the decoy) is not checked directly: a correct report may name that file while dismissing it, and a pattern cannot tell the two apart.

## Tuning exposure

This fixture is not held out. It was run against skill drafts 3, 4 and 5 during the design 0.5.0 tuning, and its results drove changes in drafts 4, 5 and 6. The released 0.5.0 text was never run on it before this case existed. *branch* as a gap, *grace period* and the *due slip* rename each flipped between those runs.
