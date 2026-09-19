/**
 * A library location where items are shelved, lent and returned, and where
 * patrons collect held items.
 *
 * Named BranchSite rather than Branch because "branch" already means a git
 * branch throughout our release tooling; see docs/conventions.md.
 */
export class BranchSite {
  constructor(
    readonly id: string,
    readonly name: string,
    readonly address: string,
  ) {}
}
