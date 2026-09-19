/**
 * Renewing and extending loans. (lexicon: renew)
 *
 * Both move the due date, but they are not interchangeable: a renewal
 * restarts the loan period from today and counts toward loans.maxRenewals;
 * an extension adds days to the current due date and does not count as a
 * renewal.
 */
import { config } from "../config";
import type { RequestContext } from "../http/context";
import type { Loan } from "./loan";

/** Response body returned to the API client after a successful renewal. */
export interface Renewal {
  loanId: string;
  renewedAt: string;
  previousDueDate: string;
  newDueDate: string;
}

export function renew(ctx: RequestContext, loan: Loan, holdsWaiting: number): Renewal {
  if (holdsWaiting > 0) throw new Error("title has holds waiting"); // ADR-0004
  if (loan.renewalCount >= config.loans.maxRenewals) throw new Error("renewal limit reached");
  const previousDueDate = loan.dueDate;
  const due = ctx.now();
  due.setUTCDate(due.getUTCDate() + config.loans.loanPeriodDays);
  loan.dueDate = due.toISOString().slice(0, 10);
  loan.renewalCount += 1;
  return { loanId: loan.id, renewedAt: ctx.now().toISOString(), previousDueDate, newDueDate: loan.dueDate };
}

export function extend(ctx: RequestContext, loan: Loan, days: number): void {
  if (days < 1 || days > config.loans.maxExtensionDays) throw new Error("extension out of range");
  const due = new Date(loan.dueDate);
  due.setUTCDate(due.getUTCDate() + days);
  loan.dueDate = due.toISOString().slice(0, 10);
  ctx.log("loan extended", { loanId: loan.id, days });
}
