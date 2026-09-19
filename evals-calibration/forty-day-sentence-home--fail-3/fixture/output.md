Consolidated. `docs/glossary.md` is the only file I touched: **22 entries → 14**.

## Verdicts

**keep (3)** — passes all three tests, already in shape

| Entry | Reason |
|---|---|
| cow | Test 2: narrower than ordinary (a female that has calved) and fixed against *heifer*; matches `IsCow` at `internal/herd/animal.go:44`. |
| farm | Test 2: the business, not the holding — the one unit whose settings and *herd* an installation holds. Weakest keep; see open questions. |
| management group | Test 2: narrower than "group", and "exactly one at a time" is meaning; matches `internal/herd/group.go:40`. |

**rewrite (8)** — term passes, definition was carrying code, config or behaviour

| Entry | Reason |
|---|---|
| dry off | Named `LactationService`; "about two months" is the `dry_period_days` default. |
| dry period | 8 sentences of mechanism, config, list behaviour and release history. |
| heifer | Was the redirect "See *cow*" — a distinct term (test 1+2) missing its entry, so written as one. |
| lactation | Named *ListBuilder* and described what lists print. |
| milking | Listed the record's fields; the *session* overload was stated only in *session*, so both now name each other. |
| parity | Absorbs the *lactation number* merge as a "not used" note. |
| session | "two or three a day" is `sessions_per_day`. |
| VWP | "Set per *farm*" is `vwp_days`. |

**rename (1, awaiting sign-off)** — test 3, headword the sources don't use

- **days in lactation → days in milk.** Every source says days in milk / DIM: `internal/lactation/lactation.go:39`, `internal/lists/builder.go:17`, `docs/configuration.md:22`, `README.md:14`, `docs/decisions/0003-dry-off-date-from-expected-calving.md:23`. "days in lactation" occurs nowhere but the glossary itself, so the rename breaks nothing.

**rename + rewrite (1, awaiting sign-off)**

- **withdrawal period → withdrawal.** "withdrawal period" appears only in the glossary; code and docs say *withdrawal*, *milk withdrawal*, *meat withdrawal*. Body rewritten around the milk/meat distinction (drift 2).

**merge (1)** — test 3

- **lactation number → parity.** One concept, one integer: `Lactation.Parity` is set from the raised parity at `internal/lactation/lactation.go:71-75`, and parity is the word every source uses. "lactation number" appears nowhere outside the glossary; recorded in *parity* as not used.

**reframe (2)** — fails test 1, but a concept behind it needed a word

- **HerdStore → new entry *herd*** (awaiting sign-off). The store is code; *herd* is the domain word the references use in a narrower sense than ordinary — membership runs from birth or purchase until she leaves, and a cull-marked cow is still in it (`internal/herd/animal.go:31-32`, `:49-51`, `internal/herd/store.go:48`).
- **withhold sweep → *withdrawal***. The sweep is a pass in the code (`internal/treatment/withdrawal.go:89-92`); the guarantee a user relies on — a milk withdrawal keeps her milk out of the saleable total — now sits in *withdrawal*.

**retire (6)** — fails test 1 or 2, nothing behind it needs a word

| Entry | Where the word belongs instead |
|---|---|
| Env | The struct: `internal/env/env.go:48-55`, plus `docs/conventions.md:20-21`. |
| GroupManager | `internal/herd/group.go:29-38`; the concept is *management group*. |
| HerdStore | See reframe above. |
| late-reading rule | A named decision, not a word: `docs/decisions/0002-late-readings-belong-to-their-session.md:20-25`, `internal/milking/ingest.go:35-37`. |
| ListBuilder | `internal/lists/builder.go:22-23`; the lists are documented in `docs/configuration.md:20-49`. |
| MeterIngest | `internal/milking/ingest.go:18-20`. |
| user | Test 2: ordinary sense, and Byre has no accounts or roles (`README.md:45`). *herd manager* stays ordinary too — it fixes nothing. |

## Where the cut content already lives

- dry off / `LactationService` → `internal/lactation/lactation.go:83-99`; "two months" → `docs/configuration.md:14`.
- dry period: target and default → `docs/configuration.md:14`, `internal/env/env.go:15-17`; due dry-off date counted back from expected calving → `docs/decisions/0003…:19-21`, `internal/lactation/breeding.go:64-68`; seven days' notice → `docs/configuration.md:15`, `internal/lists/builder.go:45`; no service ⇒ never on the list → `docs/decisions/0003…:27-28`, `docs/configuration.md:33-35`.
- Env's "nothing reads the time or a setting except through it" → `docs/conventions.md:20-21`.
- GroupManager's suggestions and move history → `internal/herd/group.go:21-27`, `:63-66`, `README.md:24-26`.
- HerdStore's "every read and write goes through it" → `internal/herd/store.go:15-16`, `docs/conventions.md:22-26`.
- lactation's "DIM on every list" → `docs/configuration.md:22`, `cmd/byre/main.go:90`.
- late-reading rule → ADR 0002 in full.
- ListBuilder's five lists and "built afresh" → `docs/configuration.md:20-49`.
- MeterIngest's reading→milking → `internal/milking/ingest.go:38-69`.
- session's 2-or-3 → `docs/configuration.md:11`, `internal/env/env.go:88-90`.
- VWP's "set per farm" → `docs/configuration.md:16`.
- withhold sweep's guarantee → ADR 0001 and *withdrawal*; its timing claim is disputed (drift 6) and deliberately not carried anywhere.

**Homeless — two items.** First, from *dry period*: "A cow whose dry period will be shorter than 40 days is marked as short on the calving list." No document or comment gives that threshold. Second, and it is a decision: the dry-period history. *"The default was 56 days until release 2.3, when it was raised to 60 because cows calving a few days early kept falling inside the 54-day minimum of the dry cow tubes in use."* Nothing else records it. `internal/env/env.go:15-17` only says "This default has history; do not change it without asking the herd manager" — it points at the reason without stating it. **This wants a decision record before the sentence is lost.** It is the one thing I cut that had no other home.

## Drift — glossary vs. code and docs

1. **days in lactation / days in milk** — headword, evidence above. Also `docs/conventions.md:7-9` says identifiers take their words from the glossary, so the code following "days in lactation" would have meant renaming `DaysInMilk`; the sources are unanimous the other way.
2. **"always withheld… never counted as saleable"** — false for meat. `docs/decisions/0001…:26-28`: *"Only a milk withdrawal puts a cow on the withhold list… A meat withdrawal never does"*; `docs/configuration.md:47-49`; `internal/treatment/withdrawal.go:16-19`. The old entry predates ADR 0001 and treated withdrawal as one thing. Sources being unanimous, I wrote the entry to match them rather than leaving the universal standing — flagging it because it is the largest change in meaning in the file.
3. **Does a session close?** `docs/configuration.md:12` says *"A session closes this long after its last milking"*, but `SessionCloseMinutes` is read and never used — its only occurrences are `internal/env/env.go:22`, `:33`, `:67`. Session membership comes from clock boundaries (`internal/milking/session.go:41-58`) and "late" means "taken in an earlier session than the clock's" (`internal/milking/ingest.go:73-76`). Either the setting is dead or the closing rule is unimplemented. **Your call** — the surviving *session* entry asserts nothing about closing.
4. **Short dry period** — the glossary said "a cow whose dry period *will be* shorter than 40 days"; `internal/lists/builder.go:54` marks it only when `s.l.Dry()`, i.e. only cows already dried off, measured from the actual dry-off date. A milking cow heading for a short dry period is never marked. Separately, `docs/configuration.md:37-39` describes the calving list without the mark at all, so a user reading the reference does not know it exists. **Your call** on which behaviour is intended.
5. **DIM for a dry cow** — the entry says "a dry cow has none"; `internal/lactation/lactation.go:39-44` returns 0, the same value a cow calved today gets, and `cmd/byre/main.go:90` prints `DIM 0` on every row, while `docs/configuration.md:22` says DIM is shown only "for a cow in lactation". **Your call**; the entry keeps "has none" meanwhile.
6. **Withhold sweep timing** — the retired entry claimed the sweep runs "when a *session* opens" and that therefore a cow is on the list "before the first cluster goes on". In fact it also runs after every treatment (`internal/treatment/withdrawal.go:65`, `:89-91`) and at start-up (`cmd/byre/main.go:58`), and the session-open sweep fires when the **first reading of the session arrives** (`internal/milking/ingest.go:25-27`) — after the first cow is on. The completeness claim in `docs/configuration.md:26-29` rests on the per-treatment sweep, not the session one. Also, "no *milking* of hers is counted towards the tank" has an exception: `docs/decisions/0002…:32-35` files a late milking's withheld mark as the list stood **on arrival**, so a withdrawal that ended in between lets it count as saleable. Not carried into any entry.
7. **VWP: "deliberately not served"** — nothing stops a service; `internal/lactation/breeding.go:26-33` records one with no VWP check, and `docs/configuration.md:16` says only that she is "not put on the serve list until she is this many days in milk". "Even if she is seen in heat" is also unrecordable — Byre has no heat record. I left the wording unchanged in substance, as it is the entry's meaning. **Your call**: farm practice or what Byre does.
8. **"seven days"** — the old *dry period* entry hardcoded the `dry_off_notice_days` default (`docs/configuration.md:15`, `internal/lists/builder.go:45`). Cut.
9. **Env "every operation"** — `docs/conventions.md:20-21` and `internal/env/env.go:48-49` qualify it to operations needing a setting, the time or the database; `docs/conventions.md:24-26` exempts record types (`DaysInMilk`, `AgeMonths`, `IsHeifer`). The entry's universal was wrong; retired anyway.

## References outside the glossary to words I retired

List only — I changed nothing outside `docs/glossary.md`.

- `internal/env/env.go:49` — `(glossary: Env)`, cites a retired word.
- `internal/treatment/withdrawal.go:90` — `(glossary: withhold sweep)`, cites a retired word.
- `docs/configuration.md:29` — "It is rebuilt by the withhold sweep when a session opens", uses a retired word as if defined, and is part of drift 6.
- **`docs/conventions.md:10-11`** — *"Every new exported type gets a glossary entry in the same pull request."* This is the rule that produced *Env*, *GroupManager*, *HerdStore*, *ListBuilder* and *MeterIngest*, and it contradicts test 1. Without changing it the glossary refills. Highest-value fix outside the glossary.
- `docs/conventions.md:7-9` — "Identifiers take their words from the glossary" is the right direction and can stand, but it now points at a glossary holding no type names.
- `README.md:32` — "the words we use, in the office and in the code" advertises the old scope.
- `internal/herd/animal.go:24` — `(glossary: parity)` is still valid.
- `docs/decisions/0003…:19` names `LactationService`; fine in a decision record, no action.

Adjacent, not glossary drift: `internal/herd/group.go:12-17` requires milkers/dry/close-up to be among the farm's groups and `Suggest` can return one (`:67-79`) that `MoveTo` would reject (`:43-45`), while `docs/configuration.md:18` never states the requirement.

## Gaps proposed (written on the gaps line, not admitted)

1. **service** — the breeding sense, used undefined throughout `docs/configuration.md:13,16,34,41-42,62` and ADR 0003. `docs/conventions.md:12-14` records that `Insemination` exists *to avoid* the word because `Service` already means a component — a collision the project itself documents, which is exactly test 2. Strongest gap.
2. **saleable** — two senses in the system: milk fit to sell (`internal/milking/session.go:63`, `internal/treatment/withdrawal.go:16`) and an animal fit to sell for slaughter (`internal/lists/builder.go:82`, `docs/configuration.md:46`, `docs/decisions/0001…:27-28`). The surviving *withdrawal* entry now uses both senses in one sentence.
3. **reading** — what the meter sends, distinct from the *milking* Byre makes from it; it can arrive late or be unusable. Met by users at `docs/configuration.md:12` and `:55`, undefined.
4. **in calf** — `docs/configuration.md:37` ("in-calf heifer") and `:42` ("no pregnancy confirmed") versus `internal/lactation/breeding.go:19-21` (`Confirmed`, set by the vet's diagnosis). Served and in calf are different states with different list consequences. Weakest of the four.

I did not propose *ear tag*, *treatment* or *herd manager*: ordinary sense covers them, and what is special about ear tags ("never parse them; farms reuse and reformat them") is a convention, already at `docs/conventions.md:16`.

## Talking in it

Sentences I tested: *"4172 is 210 days in milk and still not in calf — why isn't she on the serve list?"*, *"She was treated last night; is her milk saleable this morning?"*, *"Why did 3081's due dry-off date move?"*, *"The AM session changed after I printed the yield — a reading came in late."*, *"This counts a withheld milking towards the saleable total; a milk withdrawal must keep it out."* All say what they mean except where *in calf*, *saleable* and *reading* are missing — which is how those three reached the gaps list rather than by brainstorming. The withhold question *"is a cow with only a meat withdrawal on the withhold list?"* is answerable from the *withdrawal* entry now; it was not before.

## Needs a decision from you

1. Rename **days in lactation → days in milk** (written in, awaiting sign-off).
2. Rename **withdrawal period → withdrawal** (written in).
3. New entry **herd** from the HerdStore reframe (written in).
4. **withdrawal**: one entry naming both kinds, as written (~60 words, over the fifty-word guide), or split into *milk withdrawal* and *meat withdrawal* each naming the other? It is the highest-value distinction in the file and I could argue it either way.
5. **VWP** wording: the farm's practice ("not served") or what Byre does ("not put on the serve list")? Left as it was.
6. **farm**: keep or retire? It passes on "the business, not the holding, and one to an installation" and on nothing else.
7. Drift 3, 4, 5 and 7: code or docs — which side is right.
8. The homeless dry-period history wants a decision record. I did not write it.
