# Shelfwise lexicon

Provenance: started at the 2023 design review; entries added as ADRs landed and as the team named things in code review.
Gaps: none.

A term is admitted when the team uses it in discussion or a decision defined it.

---

**book** — A bound printed publication. Most items in Shelfwise are books, though the catalog also holds DVDs and audiobooks.

**borrower** — A person who borrows items from the library; the holder of a loan.

**catalog** — The library's record of every title and its items. Searched through the CatalogIndex.

**CatalogIndex** — The in-memory search index over titles, rebuilt at startup and after each catalog import so that searches never touch the database.

**charge sweep** — The nightly pass in LoanReconciler over loans returned in the last 24 hours that lowers each loan's fine to what was owed at the recorded return time. Returns scanned at a branch while it is offline reach the server late; the charge sweep makes sure a returned item is never still charged. See ADR-0001.

**date** — A calendar day. All dates are stored as ISO-8601 strings in UTC.

**due date** — The date by which a loan's item should be returned. Set to the checkout date plus `loans.loanPeriodDays`; moved by renewing or extending.

**due slip** — The record given to a patron at each checkout or renewal, listing every item and its due date. Stored per ADR-0005 so patrons can look up past due slips.

**extend** — To push a loan's due date back by a number of days, at most `loans.maxExtensionDays`.

**fine** — The amount a patron owes for an overdue loan, accrued at `fines.dailyRateCents` per overdue day.

**FineCalculator** — Applies one day of fine accrual to each overdue loan; runs nightly before the LoanReconciler.

**grace period** — The number of days after the due date before a loan counts as overdue and fines start. Each library sets it with `loans.gracePeriodDays` (default 2).

**hold** — A patron's request for the next available item of a title, collected at a pickup branch they choose. HoldManager allocates each returned item to the oldest waiting hold on its title.

**hold queue** — The waiting holds on a title, in the order they were placed; served first come, first served (ADR-0003).

**HoldManager** — Owns the hold lifecycle: places holds, allocates returned items to the head of the hold queue, marks holds ready, and lapses uncollected ones.

**item** — One physical copy of a title, with its own barcode. Loans are of items; holds are of titles.

**library card** — The card that identifies a patron. A card is active, suspended or expired.

**loan** — The lending of one item to one patron, from checkout until return. Persisted through the LoanRepository.

**LoanReconciler** — The nightly job that runs the charge sweep, scheduled by `reconciler.sweepCron`.

**member** — See *patron*.

**NotificationQueue** — The outbound queue for patron notices by email and SMS, retried with exponential backoff.

**overdue** — A loan is overdue once its due date plus the grace period has passed and the item has not been returned. An overdue loan always accrues a fine until the item is returned.

**patron** — A person registered with the library, identified by a library card.

**patron-first policy** — The rule from ADR-0004: when a patron wants to renew a loan whose title another patron has on hold, the hold wins and the renewal is refused.

**pickup window** — The period a patron has to collect an item that is being held for them at their pickup branch. The window length is set by `holds.pickupWindowDays` (default 7). The window starts when the item is checked in at the pickup branch, not when the patron is notified. HoldManager marks the hold ready and the NotificationQueue tells the patron at once, then reminds them the day before the window closes. When the window lapses, the hold lapses and the item passes to the next hold in the title's hold queue; the patron keeps no place in the queue (ADR-0003). The window was shortened from ten days to seven after the 2023 pilot, when uncollected holds tied up popular titles for weeks. Staff cannot lengthen an individual patron's window; a patron who misses it must place a new hold.

**renew** — To restart a loan's period from today, giving the patron a fresh full loan period. Counts against `loans.maxRenewals` (default 3). Not the same as *extend*. Implemented by `renew()`, which returns a `Renewal`.

**repository layer** — The persistence abstraction (`Repository<T>` and one implementation per aggregate); all reads and writes go through it.

**request context (ctx)** — The object passed as the first argument to every handler, carrying the signed-in patron, the site the request came from, and the clock. Written `ctx` throughout the code.

**return** — Checking an item back in at any branch, which ends its loan.

**title** — A work as the library catalogs it: one edition, one ISBN. Holds are placed on titles.

**waive** — For staff to cancel a loan's fine in full; a waived fine no longer accrues.
