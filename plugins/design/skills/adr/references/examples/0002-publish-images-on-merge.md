# ADR-0002 — Publish images on merge

**Status:** Accepted (2026-06-18) · **Supersedes:** part of [ADR-0001](0001-publish-images-on-merge-and-publisher-identity.md)

## Context

Services are deployed from container images, and a registry tag must correspond
to a merged commit rather than to whatever was on a developer machine.

ADR-0001 decided both this and the identity CI publishes as. The two are
independent: the trigger does not depend on the credential form, and the
credential form has since changed (ADR-0003) while the trigger has not. ADR-0001
is therefore split, and this ADR carries its publishing decision forward
unchanged.

## Decision

**Publish on merge to `main`.** CI builds the image and pushes it tagged with the
commit SHA. No other path writes to the registry.

## Consequences

- Every registry tag corresponds to a merged commit.
- Publishing from a developer machine is not possible; a broken CI pipeline
  blocks all releases for that service.
