/**
 * A receipt lists the items a patron checked out or renewed in one
 * transaction, with each item's due date. Receipts are kept so patrons can
 * view past ones (ADR-0005).
 */
import type { RequestContext } from "../http/context";

export interface Receipt {
  id: string;
  patronId: string;
  issuedAt: string;
  kind: "checkout" | "renewal";
  lines: { itemId: string; title: string; dueDate: string }[];
}

export function issueReceipt(ctx: RequestContext, kind: Receipt["kind"], lines: Receipt["lines"]): Receipt {
  return { id: crypto.randomUUID(), patronId: ctx.patron!.id, issuedAt: ctx.now().toISOString(), kind, lines };
}
