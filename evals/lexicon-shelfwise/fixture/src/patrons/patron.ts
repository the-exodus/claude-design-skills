import type { RequestContext } from "../http/context";

export type CardStatus = "active" | "suspended" | "expired";

/** A person registered with the library, identified by their library card. */
export interface Patron {
  id: string;
  name: string;
  homeBranchId: string;
  card: { number: string; status: CardStatus; expiresOn: string };
}

/**
 * A member is a patron whose library card is active. Only members may
 * borrow items or place holds; a patron with a suspended or expired card
 * can still sign in, see their loans and pay fines.
 */
export function isMember(patron: Patron): boolean {
  return patron.card.status === "active";
}

export function requireMember(ctx: RequestContext): Patron {
  const patron = ctx.patron;
  if (!patron || !isMember(patron)) throw new Error("not a member");
  return patron;
}
