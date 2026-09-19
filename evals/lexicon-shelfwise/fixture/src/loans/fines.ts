import { config } from "../config";
import type { RequestContext } from "../http/context";
import { isOverdue, type Loan } from "./loan";

/** Where an overdue loan stands with respect to its fine. See ADR-0002. */
export enum OverdueState {
  /** The fine grows by fines.dailyRateCents each day. */
  Accruing = "accruing",
  /** The fine has reached fines.capCents and no longer grows. */
  Capped = "capped",
  /** Staff waived the fine; nothing accrues. */
  Waived = "waived",
}

/** Nightly fine run over open loans. */
export class FineCalculator {
  runNightly(ctx: RequestContext, openLoans: Loan[]): void {
    for (const loan of openLoans) {
      if (!isOverdue(loan, ctx.now())) continue;
      loan.overdueState ??= OverdueState.Accruing;
      this.accrueOneDay(loan);
    }
  }

  accrueOneDay(loan: Loan): void {
    if (loan.overdueState !== OverdueState.Accruing) return;
    loan.fineCents = Math.min(loan.fineCents + config.fines.dailyRateCents, config.fines.capCents);
    if (loan.fineCents === config.fines.capCents) loan.overdueState = OverdueState.Capped;
  }
}

/** The fine a loan should carry for overdue days up to `until`. */
export function fineOwedAt(loan: Loan, until: Date): number {
  if (loan.overdueState === OverdueState.Waived) return 0;
  const start = new Date(loan.dueDate);
  start.setUTCDate(start.getUTCDate() + config.loans.gracePeriodDays);
  const days = Math.max(0, Math.floor((until.getTime() - start.getTime()) / 86_400_000));
  return Math.min(days * config.fines.dailyRateCents, config.fines.capCents);
}

export function waive(ctx: RequestContext, loan: Loan): void {
  loan.fineCents = 0;
  loan.overdueState = OverdueState.Waived;
  ctx.log("fine waived", { loanId: loan.id });
}
