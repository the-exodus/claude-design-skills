# ADR-0003 — Publisher identity federated over OIDC

**Status:** Accepted (2026-06-18) · **Epic:** KEY-1234 · **Supersedes:** part of [ADR-0001](0001-publish-images-on-merge-and-publisher-identity.md)

## Context

ADR-0001 gave the publisher a static registry credential held as a CI secret and
rotated quarterly. It named no owner for the rotation, and two consecutive
rotations were missed. The registry now supports OIDC federation from the CI
provider, which did not exist when ADR-0001 was written.

## Decision

**The publisher authenticates by OIDC federation from CI.** No long-lived
credential exists. The trust relationship is scoped to the service's repository
and to the `main` branch ref; a workflow running on any other ref receives no
token.

## Consequences

- There is no credential to rotate, leak, or hold in a CI secret.
- The federation subject is tied to the repository name and branch ref. Renaming
  the repository or changing the release branch breaks publishing until the
  subject is updated, and the failure appears at push time rather than at
  configuration time.
- The registry must remain reachable over the CI provider's OIDC issuer;
  publishing from anywhere without that issuer is not possible.
