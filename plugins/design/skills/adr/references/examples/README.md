# Architecture Decision Records

This directory holds Architecture Decision Records (ADRs) in Michael Nygard's
lightweight format: a short **Context / Decision / Consequences** note per
decision, with a **Status**.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-publish-cross-service-events-on-a-message-bus.md) | Publish cross-service events on a message bus | Accepted |
| [0002](0002-use-rabbitmq-as-the-message-bus.md) | Use RabbitMQ as the message bus | Superseded by ADR-0004 |
| [0003](0003-share-one-database-across-reporting-services.md) | Share one database across reporting services | Rejected |
| [0004](0004-use-azure-service-bus-as-the-message-bus.md) | Use Azure Service Bus as the message bus | Accepted |

## Conventions

- This index is the canonical list of ADRs; keep it in step with the files.
- Filenames: `NNNN-kebab-case-title.md`, numbered sequentially.
- An ADR records one decision that is architecturally significant and hard to
  change later.
- Status is one of: Proposed, Accepted, Rejected, Deprecated, Superseded.
- An Accepted ADR's body is never rewritten. A new ADR supersedes it when the
  decision is overturned or changes in substance; anything else is appended as a
  dated addendum. Implementation is tracked wherever the project tracks work,
  not here.
