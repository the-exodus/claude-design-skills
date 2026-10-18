# ADR-0002 — Use RabbitMQ as the message bus

**Status:** Superseded by [ADR-0004](0004-use-azure-service-bus-as-the-message-bus.md) (2026-09-30)

## Context

[ADR-0001](0001-publish-cross-service-events-on-a-message-bus.md) requires a
message bus. Services run on one Kubernetes cluster in a single region. The team
already operates RabbitMQ for the render job queue. Projected volume is 40
million messages a month.

## Decision

**RabbitMQ, self-hosted on the cluster.**

Rejected: Azure Service Bus. At the projected volume, its per-message pricing
exceeds the budget for the bus several times over.

## Consequences

- The team operates the broker: upgrades, capacity, and backup of its
  definitions.
- Services use AMQP 0-9-1 clients. Changing broker means changing the messaging
  client in every service.
- The broker lives in one region. Running services in a second region needs
  cross-region federation, which this decision does not provide.
