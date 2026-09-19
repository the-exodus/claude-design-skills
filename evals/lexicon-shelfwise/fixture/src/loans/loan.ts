import { config } from "../config";
import type { OverdueState } from "./fines";

/** The lending of one item to one patron, from checkout until return. */
export interface Loan {
  id: string;
  itemId: string;
  patronId: string;
  checkedOutAt: string;
  dueDate: string;
  renewalCount: number;
  returnedAt?: string;
  fineCents: number;
  /** Undefined until the loan first becomes overdue. */
  overdueState?: OverdueState;
}

/**
 * A loan is overdue once its due date plus the grace period has passed
 * and the item has not been returned.
 */
export function isOverdue(loan: Loan, today: Date): boolean {
  if (loan.returnedAt) return false;
  const limit = new Date(loan.dueDate);
  limit.setUTCDate(limit.getUTCDate() + config.loans.gracePeriodDays);
  return today > limit;
}
