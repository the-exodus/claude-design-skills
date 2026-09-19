import type { Patron } from "../patrons/patron";
import type { BranchSite } from "../branches/branch-site";

/**
 * Per-request state handed to every handler as its first argument, `ctx`.
 * Built by the HTTP middleware from the session cookie and the terminal id.
 */
export interface RequestContext {
  /** The signed-in patron, or undefined on a staff terminal. */
  patron?: Patron;
  /** The site the request came from. */
  site: BranchSite;
  /** Injected clock so tests can pin "today". */
  now(): Date;
  log(msg: string, fields?: Record<string, unknown>): void;
}
