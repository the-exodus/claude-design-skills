**31 entries → 17.** `docs/design/lexicon.md` is the only file changed.

## Verdicts

**Keep (2)** — passes all three tests, already in shape (italics only):

| Entry | Reason |
|---|---|
| **item** | Physical copy vs *title* is the distinction the whole catalog is reasoned in. |
| **loan** | Central domain concept; only the `LoanRepository` mention had to go (so, strictly, a one-clause rewrite). |

**Rewrite (13)** — term passes, definition carried code, config keys or behaviour:

| Entry | Reason |
|---|---|
| **due date** | Dropped `loans.loanPeriodDays` (a reference's job); kept the grace-period distinction. |
| **extend** | Dropped `loans.maxExtensionDays`; kept the distinction from *renew*, which is why it exists. |
| **fine** | Dropped the daily rate; kept the per-loan boundary, which is what the domain fixes. |
| **grace period** | Dropped the config key and default; the boundary it fixes is the meaning. |
| **hold** | Cut the `HoldManager` allocation sentence; kept request, title, pickup branch. |
| **hold queue** | Kept ordering and the lapse exception; "first come, first served" was restating the order. |
| **member** | Was a redirect to *patron*, but the sources treat it as a strict subset — a distinct term missing its entry (test 3's redirect rule). |
| **overdue** | Definition matches the code; the false universal removed (drift D1). |
| **patron** | Now names the *member* distinction and records "borrower" as not used. |
| **pickup window** | 120 words of schedule, notices, history and staff policy cut to meaning: when the clock starts, and what lapsing costs. |
| **renew** | Dropped `renew()`/`Renewal` and the config key; kept the *extend* distinction and the hold precedence. |
| **return** | Added the clause that makes it pass test 2: a return counts from the scan time, not the sync time (ADR-0001). |
| **title** | Stated the overload the entry never did: a title is the work, not the work's name (`src/catalog/title.ts:5` has `name` on `Title`). |
| **waive** | Kept "in full"; the distinction from a capped fine is what it is easily conflated with. |

**Rename (1, awaiting your confirmation)**

- **due slip → receipt** — no source uses "due slip" except ADR-0005's account of what came before: `README.md:6`, `docs/api.md:31-34`, `docs/adr/0005-keep-receipts.md:16-18`, `src/receipts/receipt.ts:8`. Written under *receipt*, with "due slip is not used" recorded. Say the word if you want it back.

**Merge (1)** — test 3

- **borrower → patron** — same concept, and no source uses "borrower"; the code carries `patronId` (`src/loans/loan.ts:8`, `src/holds/hold.ts:7`). Recorded in *patron* as not used.

**Retire (14)**

Fails test 1 (names a part of the code):

| Entry | Where the word belongs |
|---|---|
| **CatalogIndex** | `src/catalog/catalog-index.ts:4-7` — the doc comment already says all of it. |
| **charge sweep** | The mechanism; the guarantee it serves is in `docs/api.md:20-21`, the mechanism in ADR-0001 and `src/loans/loan-reconciler.ts:1-8`. |
| **FineCalculator** | `src/loans/fines.ts:15-16`; its ordering before the reconciler is ADR-0001:27-28. |
| **HoldManager** | `src/holds/hold-manager.ts:1-4`; the concept is already carried by *hold* and *hold queue*. |
| **LoanReconciler** | `src/loans/loan-reconciler.ts:13`; its schedule is `docs/configuration.md:32`. |
| **NotificationQueue** | `src/notifications/notification-queue.ts:1-6`. |
| **repository layer** | `docs/conventions.md:9` and `src/storage/repository.ts:4` — project convention, not domain language. |
| **request context (ctx)** | `docs/conventions.md:8` and `src/http/context.ts:4-7`. |

Fails test 2 (ordinary sense):

| Entry | Where the word belongs |
|---|---|
| **book** | A format value, `src/catalog/title.ts:6`. Ordinary word otherwise. |
| **catalog** | Ordinary in a library; "searched through the CatalogIndex" is code. |
| **date** | The ISO-8601/UTC part is a convention: `docs/conventions.md:10`. |
| **library card** | Ordinary; the three statuses are `src/patrons/patron.ts:3`. *member* now carries the only part that mattered. |
| **patron-first policy** | Its whole content is a decision: ADR-0004. Also misnamed — both parties are patrons; the rule is that holds beat renewals. |
| **due slip** | (Retired as a headword — see the rename above.) |

## Content cut, and where it already lives

Every cut sentence has a home except one. Of note, the window starting at check-in, not at notification → `src/notifications/notification-queue.ts:4-5`. Spot checks: hold allocation → ADR-0003:17 and `src/holds/hold-manager.ts:25-27`; pickup notices → ADR-0003:19-21 and `src/notifications/notification-queue.ts:3-5`; "staff cannot lengthen an individual window" → ADR-0003:26; fine cap and states → ADR-0002:17-21 and `src/loans/fines.ts:6-13`; every config key and default → `docs/configuration.md:10-32`; "a returned item is never still charged" → `docs/api.md:20-21`.

**Homeless (1):** from *pickup window* — "The window was shortened from ten days to seven after the 2023 pilot, when uncollected holds tied up popular titles for weeks." ADR-0003 records the fixed window but not the change from ten days or why. `src/config.ts:15-17` gestures at it ("Changing the default has history; ask the circulation team"). This is a missing decision record — an amendment to ADR-0003, or a superseding record. I have not written it; it is now recorded nowhere but this report.

## Drift — your call, I did not settle these

**D1. An overdue loan does not always accrue a fine.**
Old entry: "An overdue loan always accrues a fine until the item is returned."
Against: `docs/adr/0002-cap-overdue-fines.md:24-25` — "An overdue loan no longer necessarily accrues a fine: it may be accruing, capped or waived"; `src/loans/fines.ts:6-13` (the three `OverdueState` cases), `src/loans/fines.ts:26-28` (accrual stops at the cap), `src/loans/fines.ts:34` (waived owes nothing).
It is a behaviour claim, so it is not in the new entry — the lexicon simply no longer asserts it. ADR-0002 holds the truth. Nothing else to fix unless you want the ADR restated somewhere.

**D2. "A returned item is never still charged" is a universal the code does not hold at all times.**
`docs/api.md:20-21` states it absolutely. `src/loans/loan-reconciler.ts:16-26` corrects fines only on the nightly pass, and only downward; `docs/configuration.md:32` schedules that at 03:00. Between the fine run and the sweep, a returned item can show an overcharge for up to a day. The lexicon no longer makes the claim; `docs/api.md` still does, and I did not edit it.

**D3. `member` and `patron` were one word in the lexicon and two in the sources.**
`docs/api.md:3-5` and `src/patrons/patron.ts:13-24` make member a strict subset (active card) gating borrowing and holds. The old "**member** — See *patron*" erased exactly the distinction the API enforces. I wrote the entry the sources imply; if the team really does use the words interchangeably in conversation, the API is the thing to change instead.

**D4. `borrower` and `patron-first policy` appear in no source at all** — not in code, docs or ADRs. Merged and retired respectively on that basis.

## References outside the lexicon to retired words

Listed only; I changed nothing outside the lexicon.

- `src/loans/loan-reconciler.ts:2` — cites `(lexicon: charge sweep)`, now undefined.
- `src/holds/hold-manager.ts:3` — cites `(lexicon: HoldManager)`, now undefined.
- `docs/configuration.md:32` — uses "charge sweep" and "the fine run" as if both were defined terms.
- `docs/adr/0001-reconcile-returned-loans-nightly.md:20,27-28` — "the fine run", "the reconciliation job": fine as an ADR describing its own mechanism, noted only because the configuration page leans on the same phrase.
- `docs/adr/0005-keep-receipts.md:11` — "paper due slip"; historical and accurate, no change needed.
- `docs/conventions.md:3-4` — **this is what produced the code-name entries**: "If a concept has no lexicon entry yet, add one before naming it in code." It tells developers to add a lexicon entry for every code name. Unless it is amended, the lexicon will regrow `CatalogIndex` and friends. `docs/conventions.md:11` (`(lexicon: term)` doc comments) is fine as a convention but is what left the two dangling citations above.

## Gaps proposed (on the Gaps line, not admitted)

- **branch** — `BranchSite` exists purely to avoid the word (`src/branches/branch-site.ts:5-6`, `docs/conventions.md:5-7`), and *hold*, *pickup window* and *return* all use "branch" undefined. A domain word a component was named to dodge.
- **ready** — `docs/api.md:28`, `src/holds/hold.ts:11` and the *pickup window* entry all lean on it in a narrow sense: set aside for one patron at their pickup branch, window running. Undefined today.
- **capped fine** — *waive* now distinguishes waived from capped, and ADR-0002:26 says reports must show which of the three states a loan is in, but no entry defines the capped one. Admit it or drop the clause from *waive*.

## Talking in it

"Her card expired so she's not a member any more — she can still pay fines but can't place holds." "The item came back Friday; the return counts from the scan, so the weekend shouldn't be fined." "Renewal's refused because the title has a hold waiting — offer an extension." "The pickup window lapsed Tuesday and the item went to the next hold in the queue; she keeps no place." All of these say themselves.

One sentence still doesn't: "It's been overdue a week and the fine hasn't moved." Capped or waived? That is gap 3, and it is the one place the consolidated lexicon leaves a real question unanswerable.
