# Architecture Decision Records

This directory holds Architecture Decision Records (ADRs) in Michael Nygard's
lightweight format: a short **Context / Decision / Consequences** note per
decision, with a **Status**.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-publish-images-on-merge-and-publisher-identity.md) | Publish images on merge; least-privilege publisher identity | Superseded by ADR-0002 and ADR-0003 |
| [0002](0002-publish-images-on-merge.md) | Publish images on merge | Accepted |
| [0003](0003-publisher-identity-federated-over-oidc.md) | Publisher identity federated over OIDC | Accepted |

## Conventions

- This index is the canonical list of ADRs; keep it in step with the files.
- Filenames: `NNNN-kebab-case-title.md`, numbered sequentially.
- Status is one of: Proposed, Accepted, Deprecated, Superseded.
- An ADR records a decision and why; it is not updated when the decision is
  implemented — supersede it with a new ADR if the decision changes.
