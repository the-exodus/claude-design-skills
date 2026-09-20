# Stockroom fixture: answer key

Fixture root: `fixture/` beside this file (all paths below are relative to it). The scaffold script copies it into the run's workspace; this file is never copied.
Lexicon: `GLOSSARY.md` (repo root, 38 entries, entries on odd lines 7–81).
Header admission rule is wrong ("appears in the code, or a decision introduced it", GLOSSARY.md:3-4); expected: replace it with the needs-defining rule and add a Gaps line (none exists).

Tests: 1 = language, not code (component names belong in the code). 2 = needs defining to talk about using or developing the system. 3 = one word per concept (synonyms merge, overloads distinguished only where people meet both senses).

## Verdict per entry

| Line | Entry | Verdict | Test | Why |
|---|---|---|---|---|
| 7 | adjustment | keep | – | Domain term (MovementKind.ADJUSTMENT, docs/api.md:21). Supports the movement drift. |
| 9 | allocation | keep | – | Must survive. The allocate/reserve distinction (allocation names bins, reservation does not) is the whole point. ADR-0001:14-16, 20. |
| 11 | AllocationEngine | retire | 1 | Class name. Mechanism sentences (earliest-expiry, skip quarantine) are in allocation.py:13 docstring. |
| 13 | available | rewrite (trim) | 2 | Bloated but correct. See the "bloated entry" section below. |
| 15 | backorder | rewrite (own definition) | 3 | A redirect stub for a distinct concept. A backorder is an order line accepted with nothing available to reserve; it has no reservation. Evidence: models.py:59, reservations.py:22-25, docs/api.md:10-11. Merging it into reservation would be wrong. |
| 17 | bin | keep | – | Core term. |
| 19 | box | retire | 2 | Ordinary word. |
| 21 | CollectionDesk | retire | 1 | Class name (despatch.py:6). The concept behind it is a collection by the carrier's *driver*, which is an ordinary word (line 27). |
| 23 | cycle count | keep | – | "done without stopping picking" reads as behaviour but IS the distinction from stocktake. Must be kept (counting.py:3-5, operators-guide.md:22-24). |
| 25 | despatch note | rewrite under **packing slip** ("despatch note" not used), flag for sign-off | 3 + drift | Code and every reference say packing slip: packing.py:1,3,11; README.md:5; ADR-0004:15; operators-guide.md:32-33. "despatch note" appears only in GLOSSARY.md:25. Also "batches" in this entry follows the batch reframe. |
| 27 | driver | retire, or keep with the sense stated | 2 | Accepted either way, by the owner's ruling of 2026-09-20 (THE-212, won't fix). Planted for THE-209 to model a held-out failure: an ordinary word, central and user-facing (the Despatch section, operators-guide.md:46-53), the concept behind a retired component (*CollectionDesk*, line 21), with the printer driver two lines further on (operators-guide.md:55-56). The unchanged skill keeps it in about half of all runs, adding "Not the printer driver", and four rewordings of the overload case did not move that. The owner's reading: where the documentation uses a bare word that can be read another way, a run that keeps the entry and says which sense is meant is doing its job. Not graded. What the driver's signature does is behaviour and lives in despatch.py:16 and the guide. |
| 29 | event bus | retire | 1 | Component (events.py:1). |
| 31 | item code | merge → SKU ("item code" not used) | 3 | Synonym. "item code" appears nowhere outside GLOSSARY.md:31. |
| 33 | movement | rewrite + drift | – | The universal "from one bin to another bin" is false: models.py:39 RECEIPT (no source bin), :42 PICK (no destination bin), :43 ADJUSTMENT (nothing moves). Enum at models.py:38-43. Surface it with file:line; do not silently settle. |
| 35 | on-hand | keep (absorbs "stock level" as not-used; may take the never-negative guarantee, see line 53) | – | Core term. |
| 37 | ORM session | retire | 1 | Component. The "never directly" rule already lives in CONTRIBUTING.md:5-6. |
| 39 | pick list | keep | – | Domain term. It uses the undefined *wave* (the gap). |
| 41 | pick queue | keep, add overload distinction (rewrite) | 3 | This overload counts. The developer meets both senses: picking.py:3-5 says it is not FIFO (ordered by wave, then walk sequence), and jobs.py:1-4 has a FIFO job queue. The entry should say it is not first-in-first-out and not the job queue. |
| 43 | PickListBuilder | retire | 1 | Class name (picking.py:22). |
| 45 | putaway | keep | – | Domain term (MovementKind.PUTAWAY). *Debatable:* retire as self-explanatory. |
| 47 | quantity | retire | 2 | Ordinary word. |
| 49 | quarantine | keep | – | Domain term. It carries the exception that available depends on. |
| 51 | receipt | keep | – | Domain term. *Debatable:* models.py:39 says RECEIPT is also used for customer returns (returns.py:12); "from a supplier" is not in the entry, so there is no hard drift. |
| 53 | reconciliation sweep | reframe → the guarantee "on-hand is never negative" (state it under on-hand, or as an entry named for the guarantee); the mechanism is cut | 1/2 | Mechanism. The mechanism lives in ADR-0003:14-17 and movements.py:3-5, and the guarantee in ADR-0003:21. **Drift:** a user doc uses the mechanism's name: operators-guide.md:27 ("kept honest by the reconciliation sweep"), when operators need only the guarantee. Surface it. *Debatable:* whether the guarantee becomes its own headword or a sentence under on-hand. |
| 55 | reservation | keep | – | Concept. Must survive with the allocation distinction. |
| 57 | reservation TTL | keep | – | Decoy. It looks technical, but operators set it (operators-guide.md:36-44) and talk about it. |
| 59 | ReservationService | retire | 1 | Component vs concept: keep *reservation*, retire the class (reservations.py:15). |
| 61 | return | keep, no overload note | – | Decoy overload. The code has function `return`s everywhere, but nobody confuses a customer return with a return value. Adding "not a function return" is wrong. |
| 63 | scan | retire | 2 | Decoy: an ordinary word with a platform sense. Planted for THE-209, after a held-out fixture showed runs keeping such a word on a platform overload. Operators scan cartons (operators-guide.md:5), and the code has the database sense (availability.py:17-18, "a sequential scan of the ledger"), but nobody talking about a warehouse confuses reading a barcode with a table scan. Keeping it, with or without a "not a database scan" note, is wrong. |
| 65 | shelf | retire | 2 | Ordinary word. Its synonym relation to *bin* ("operators sometimes say shelf") is not borne out: "shelf" appears once elsewhere, ADR-0004:9, in its ordinary sense. *Debatable:* merge into bin as "shelf (not used)". Accept either, but not a keep. |
| 67 | SKU | keep (absorbs item code) | – | |
| 69 | SkuCache | retire | 1 | Component (sku_cache.py). |
| 71 | stock | merge → on-hand ("stock level" not used) | 3 | Near-synonym that is also an ordinary word. The sources do use it as a competing word for on-hand: operators-guide.md:26 "stock level of a SKU". It should be a merge, not a plain retire. Flag operators-guide.md:26 as an outside edge. |
| 73 | StockLot | reframe → **batch** (lot); the job sense ("batch job", jobs.py:1-4, :9) is the distinguished overload | 1 + 3 | The class name exists only to dodge the domain word, and the entry says so. Operators and labels say "batch number" (operators-guide.md:5-6; ADR-0005:9-11, 19-20). Code terms: StockLot / lot_no (models.py:26-33). "lot" may be noted as the code's word. |
| 75 | stocktake | keep | – | The other half of the cycle-count distinction. |
| 77 | two-phase pick | retire | 2 | Decision-only. The phrase appears nowhere but GLOSSARY.md:77, and ADR-0004 never uses it. |
| 79 | unit of work | retire | 1 (and 2) | Decoy: identifier used everywhere (`uow()` in db.py:21, api.py:13/19/24, reservations.py:23/32, sku_cache.py:25; the phrase in events.py:4, movements.py:3, ADR-0003:14). It is a code pattern name, and pervasiveness does not make it domain language. The rule lives in CONTRIBUTING.md:5. *Debatable* only weakly. |
| 81 | zone | keep | – | Domain term. |

Tally (38; *driver* is accepted either way and counted here as retired): retire 14 (AllocationEngine, CollectionDesk, driver, event bus, ORM session, PickListBuilder, ReservationService, SkuCache, unit of work, box, quantity, scan, shelf, two-phase pick); reframe 2 (reconciliation sweep → guarantee, StockLot → batch); merge 2 (item code → SKU, stock → on-hand); rewrite 5 (available, backorder, despatch note → packing slip, movement, pick queue); keep 15.

## Bloated entry: available (GLOSSARY.md:13, 130 words)

Sentences, in order:
1. "…on-hand less everything reserved against it, **except for quarantined units, which are on-hand but never available**." Keep, **including the exception clause**. That clause is the trap: without it, "available = on-hand − reserved" is a false universal (availability.py:8 excludes quarantine bins; docs/api.md:5-6; operators-guide.md:11-12).
2. "Available is a figure for the whole warehouse, not for a bin…" Keep. It distinguishes available from on-hand, which is per bin.
3. "`available_qty()` works it out by summing the bin rows and subtracting open reservations in a single query." Cut. **Docstring-only home:** availability.py:15.
4. "It is computed on read rather than stored, as decided in ADR-0002 after the stored counter went stale during the 2024 peak." Cut. Home: docs/decisions/0002-compute-available-on-read.md:9-16.
5. "The API returns it as the `available` field of the SKU resource." Cut. Home: docs/api.md:3-6 (also schemas.py SkuOut).
6. "Sales staff should treat anything below five as 'call the warehouse' rather than promising a delivery date." Cut. **Homeless**: nothing else contains it (grep "call the warehouse", "five"). It must be listed as having no home.
7. "When a reservation lapses, its quantity is available again at once." Cut or keep; its home is the reservation TTL entry (GLOSSARY.md:57). *Debatable.*

## Drift to surface (file:line; never settle silently)

- movement's universal vs the enum: stockroom/models.py:38-43 (RECEIPT :39, PICK :42, ADJUSTMENT :43), against GLOSSARY.md:33.
- despatch note vs packing slip: GLOSSARY.md:25 vs stockroom/packing.py:1,3,11; README.md:5; docs/decisions/0004-separate-pick-and-pack.md:15; docs/operators-guide.md:32-33. Expected: write under packing slip, "despatch note" not used, flagged for sign-off.
- A mechanism name in a user doc: docs/operators-guide.md:27 "reconciliation sweep".
- The StockLot / batch naming split: stockroom/models.py:26-30 vs docs/operators-guide.md:5-6 (ADR-0005 acknowledges it). This is part of the reframe, and flagging it is good.
- *Optional:* stockroom/models.py:39 RECEIPT also covers customer returns.

## Outside edges (references to retired or renamed terms)

- stockroom/allocation.py:3 → AllocationEngine entry
- stockroom/picking.py:25 → PickListBuilder entry
- stockroom/reservations.py:16 → ReservationService entry
- stockroom/sku_cache.py:3 → SkuCache entry
- stockroom/db.py:3-5 → "unit of work and the ORM session are defined in GLOSSARY.md"
- stockroom/models.py:30 → StockLot entry (renamed to batch)
- CONTRIBUTING.md:4 "When you add a service or engine class, add a glossary entry for it." This convention contradicts test 1 and should be flagged. CONTRIBUTING.md:8 (docstrings point to glossary entries for classes) is related.
- docs/operators-guide.md:26 "stock level" (merged, not used)
- docs/operators-guide.md:27 "reconciliation sweep"
- Nothing references "despatch note", "item code" or "two-phase pick" outside the glossary.

## Gaps

- **wave**: a group of orders released and picked together. It is used undefined in README.md:5, operators-guide.md:14-18 and :44, api.md:13-15, ADR-0001:1,15,22, picking.py:3-4, api.py:23, and GLOSSARY.md:39 itself. Must be proposed.
- *Acceptable extras (debatable):* **pick task** (ADR-0004:19, api.md:15, allocation.py:14, used in 2 entries); **order line** (used in 3 entries). A proposal of either is fine but not required.

## Decoys and the fooled verdict

| Decoy | Where | Fooled verdict | Right verdict |
|---|---|---|---|
| A DTO named like a domain word | schemas.py:7 `class CycleCount` | Retire *cycle count* as a component/class name | Keep; the DTO takes its name from the term |
| A docstring that mentions the topic but not the homeless sentence | api.py:3 ("the figure sales staff look at") | Claim sentence 6 (the "below five" guidance) has a home in api.py | Sentence 6 is homeless |
| An identifier used everywhere, with an entry | `uow()` / "unit of work" (see line 79 above) | Keep because it is pervasive | Retire (test 1) |
| A user-facing term that looks technical | reservation TTL / `reservation_ttl` (operators-guide.md:36-44) | Retire as a config key or code name | Keep |
| An overload that doesn't count | return (customer) vs function `return` | Add a "not a return value" distinction | Keep as is |
| An ordinary word with a platform sense its users meet (planted for THE-209; no longer a decoy) | driver: central in the Despatch section (operators-guide.md:46-53), behind the retired *CollectionDesk*; the printer driver at operators-guide.md:55-56 | none: accepted either way | Retire, or keep with "not the printer driver" stated (THE-212, won't fix) |
| An ordinary word with a platform sense developers meet (planted for THE-209) | scan (a barcode, operators-guide.md:5) vs Postgres' sequential scan (availability.py:17) | Keep it as overloaded, with a "not a database scan" note | Retire (test 2): nobody applies the database sense to a carton |
| A clause that reads as behaviour but is the distinction | cycle count "without stopping picking" | Strip it as behaviour | Keep |
| A redirect stub | backorder "See *reservation*." | Merge into reservation | Rewrite with its own definition |
| An exception clause | available, "except for quarantined units…" | Trim it as detail | Keep; without it the entry is false |

## Debatable items (summary)

- reconciliation sweep: whether the guarantee goes under on-hand or gets its own headword.
- shelf: retire vs merge into bin as not-used.
- putaway: keep vs retire as self-explanatory.
- available sentence 7: cut (home is reservation TTL) vs keep.
- receipt: whether to flag the RECEIPT-for-returns comment at models.py:39.
- Extra gaps (pick task, order line).

## Open conflicts between this key and the runs — no judge has graded this fixture

Both tuning runs disagreed with the key on four entries, in the same direction each time. Nobody has ruled on them, so none is graded:

| Entry | Key | Both runs |
|---|---|---|
| reservation TTL | keep (decoy: user-facing) | retired |
| return | keep, no overload note | retired |
| despatch note | rename to *packing slip*, flagged for sign-off | retired (test 2 fired before the rename rule) |
| reconciliation sweep | reframe to the guarantee | retired |

By the reasoning of the Shelfwise round-3 and round-4 amendments, retiring *reconciliation sweep* with the guarantee homed (ADR-0003:21) is likely acceptable.

Owner's ruling (2026-09-19): *reservation TTL* is a keep, and graded (`user-facing-term-kept`). It has a config key, but operators set it and say it, the same plant as *grace period* in Shelfwise and *split ratio* in Tessera. Retiring it, or merging it into *reservation*, is a failure. Under the released 0.5.1 text, one run in four kept it.

The other three stay ungraded beyond what is already checked. *return* no longer conflicts: all four 0.5.1 runs kept it, and keep or retire is defensible for a near-ordinary word. For *despatch note* and *reconciliation sweep* the graders check the part that is not debatable, that the unused headword and the routine's name are gone; whether *packing slip* earns an entry, and whether the guarantee lives in the glossary or in ADR-0003, is accepted either way.

## What the graders check

Deterministic `regex` graders carry the case. They grade only what a correct run must do whichever way the debatable and the open items fall.

On the written glossary (`GLOSSARY.md`), by entry heading (`**term**` at the start of a line):

| Grader | Plant |
|---|---|
| `components-retired`, `no-code-names` | component names; `ReservationService` beside *reservation* |
| `pervasive-identifier-retired` | *unit of work*: everywhere in the code, not language |
| `ordinary-words-retired` | *box*, *quantity* |
| `decision-only-retired` | *two-phase pick* |
| `mechanism-name-retired` | *reconciliation sweep* (true under reframe and under retire) |
| `unused-headword-gone` | *despatch note* (true under rename and under retire) |
| `synonyms-merged`, `synonym-recorded-not-used` | *item code*, *stock*, *shelf*; *SKU* records "item code" |
| `dodging-component-retired`, `dodged-word-admitted` | `StockLot` reframed to *batch* |
| `distinction-allocation-names-reservation`, `distinction-reservation-names-allocation` | *allocation* / *reservation* |
| `distinction-stocktake-kept`, `cycle-count-distinction` | *cycle count* / *stocktake*, and the `CycleCount` DTO decoy |
| `redirect-rewritten-backorder` | the "See *reservation*" stub becomes a real entry |
| `user-facing-term-kept` | *reservation TTL* (owner's ruling, above) |
| `exception-kept-available` | the quarantine exception survives the trim |
| `overload-stated-pick-queue` | not FIFO, not the job queue |
| `decoy-overload-not-stated` | no "not a return value" note (passes if *return* is retired) |
| `dev-platform-sense-word-retired` | *scan* has no entry: a sense only developers meet (Postgres' sequential scan) does not make an ordinary word need defining. No run has kept it. *driver* is not graded: see its row |
| `no-entry-over-80-words`, `guidance-cut-from-entry` | the bloated *available* entry |
| `header-admission-replaced` | the header's admission rule |

On the report (the last message): `drift-movement-cited` (`models.py` at 35–43), `edge-contributing-cited` (`CONTRIBUTING.md` at 3, 4 or 8), `homeless-sales-guidance`, `gap-wave-proposed`. The glossary has no gaps line, so the gap is looked for in the report.

One narrow `llm` grader, `cycle-count-distinction`, reads the written glossary: the clause that reads as behaviour but is the distinction from *stocktake* is still there. A pattern cannot pin its wording.

Not graded: *return*, the *packing slip* entry and where the never-negative guarantee lands (above); putaway, receipt, shelf retire-vs-merge, available sentence 7, extra gaps; the docstring-only home `availability.py:15`; unplanned drift (credit, never required).

Known limits: `homeless-sales-guidance` and `gap-wave-proposed` are proximity matches in the report, so an unusual heading can fail a correct run. Whether a run cites `stockroom/api.py:3` as the guidance's home (the decoy) is not checked directly, for the same reason as in Shelfwise.

## Tuning exposure

This fixture is not held out. It was built at round 5 of the design 0.5.0 tuning, run against drafts 5 and 6, and its draft-5 results drove draft-6 changes (the batch-job overload, the backorder redirect, putaway/receipt over-pruning, the CONTRIBUTING convention edge). No iteration happened after its last run. backorder, putaway and receipt flipped between those two runs.
