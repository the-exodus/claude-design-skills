# ADR-0001 — Publish images on merge; least-privilege publisher identity

**Status:** Superseded by [ADR-0002](0002-publish-images-on-merge.md) (publishing) and [ADR-0003](0003-publisher-identity-federated-over-oidc.md) (identity), 2026-06-18

## Context

Services are deployed from container images. Nothing published them
automatically: images were built on developer machines and pushed by hand, so a
registry tag and the commit it claimed to carry could diverge, and two incidents
in the preceding quarter traced to a tag built from uncommitted work. CI already
runs on merge to `main` and a registry is in place.

## Decision

- **Publish on merge to `main`.** CI builds the image and pushes it tagged with
  the commit SHA. No other path writes to the registry.
- **Publisher identity:** a dedicated registry account holding push rights on
  the service's own repository path and no access to any other path.
  Authenticated from CI with a static credential held as a CI secret, rotated
  quarterly.

## Consequences

- Every registry tag corresponds to a merged commit.
- Quarterly rotation is manual work, and this ADR names no owner for it.
- A leaked CI secret grants push access to the service's registry path until the
  next rotation.
- Publishing from a developer machine stops working; a broken CI pipeline blocks
  all releases for that service.
