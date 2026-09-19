/**
 * A patron's request for the next available item of a title, to be
 * collected at a pickup branch.
 */
export interface Hold {
  id: string;
  patronId: string;
  titleId: string;
  pickupBranchId: string;
  placedAt: string;
  status: "waiting" | "ready" | "collected" | "lapsed";
  /** Set by HoldManager.markReadyForPickup. */
  readyAt?: string;
}
