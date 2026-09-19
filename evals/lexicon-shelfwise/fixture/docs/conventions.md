# Code conventions

- Identifiers take their names from the lexicon (`docs/design/lexicon.md`).
  If a concept has no lexicon entry yet, add one before naming it in code.
- Never name a type or variable plain `branch` or `Branch`: the word already
  means a git branch throughout our release tooling. Use `BranchSite` for a
  library location. Compound field names such as `pickupBranchId` are fine.
- Every handler takes `ctx: RequestContext` as its first parameter.
- All persistence goes through the repository layer in `src/storage`.
- Dates are ISO-8601 strings in UTC. Money is integer cents.
- Doc comments that rely on a lexicon term cite it as `(lexicon: term)`.
