# ADR-0004 — Use Azure Service Bus as the message bus

**Status:** Accepted (2026-09-30) · **Supersedes:** [ADR-0002](0002-use-rabbitmq-as-the-message-bus.md)

## Context

ADR-0002 chose self-hosted RabbitMQ in a single region and rejected Azure
Service Bus on per-message cost. Two things have changed. Services are moving to
two regions, and RabbitMQ across regions needs federation that the
team would build and operate itself, with no experience running it. The renewed
Azure agreement prices Service Bus Premium per namespace, which removes the cost
objection, and Service Bus Premium replicates between regions as a managed
feature.

## Decision

**Azure Service Bus Premium.**
[ADR-0001](0001-publish-cross-service-events-on-a-message-bus.md) is unaffected:
services still publish cross-service events to a bus.

Rejected: RabbitMQ with cross-region federation. It keeps the existing clients
but leaves the team operating a multi-region broker.

## Consequences

- There is no broker for the team to operate.
- Every service replaces its AMQP 0-9-1 client. Both buses run side by side
  until the last consumer has moved.
- The bus costs a fixed monthly amount per namespace, independent of volume.
- Messaging is tied to Azure. Moving cloud provider means changing broker again.
