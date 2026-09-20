## Consolidation report

31 entries before, 13 after.

### Verdicts
- **HoldManager** — retire (test 1): a class. **hold** — keep.
- **charge sweep** — retire; guarantee lives in docs/api.md:20-21.

### Where cut content lives
- pickup window: length key → `docs/configuration.md`:26; notices → ADR-0003:19-20, notification-queue.ts:4-5; the check-in start stays in the entry (also doc comment hold-manager.ts:26–29).

### Homeless content
- "The window was shortened from ten days to seven after the 2023 pilot, when uncollected holds tied up popular titles for weeks." — no other home. `src/config.ts` hints at history only.

### Drift
1. overdue "always accrues" vs `src/loans/fines.ts`:6–13 (enum OverdueState), and ADR-0002:24-25.
2. due slip vs receipt: src/receipts/receipt.ts:8, docs/api.md:31-34.
3. docs/configuration.md:32 names the charge sweep to users.

### Outside edges
- src/holds/hold-manager.ts:3 cites (lexicon: HoldManager)
- loan-reconciler.ts:2 cites (lexicon: charge sweep)

### Gaps
- branch
