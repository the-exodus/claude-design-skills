/**
 * Nightly reconciliation of returned loans. (lexicon: charge sweep)
 *
 * Returns scanned at a branch while it is offline reach the server late, so
 * the nightly fine run may already have charged days past the return. This
 * job resets each recently returned loan's fine to what was owed at the
 * recorded return time. See ADR-0001.
 */
import type { RequestContext } from "../http/context";
import type { LoanRepository } from "../storage/repository";
import { fineOwedAt } from "./fines";

export class LoanReconciler {
  constructor(private loans: LoanRepository) {}

  async reconcileReturnedLoans(ctx: RequestContext): Promise<number> {
    const since = new Date(ctx.now().getTime() - 24 * 3600 * 1000);
    let corrected = 0;
    for (const loan of await this.loans.returnedSince(since)) {
      const owed = fineOwedAt(loan, new Date(loan.returnedAt!));
      if (loan.fineCents > owed) {
        loan.fineCents = owed;
        await this.loans.save(loan);
        corrected++;
      }
    }
    ctx.log("reconciled returned loans", { corrected });
    return corrected;
  }
}
