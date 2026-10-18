# ADR-0001 — Publish cross-service events on a message bus

**Status:** Accepted (2026-03-02)

## Context

Services notify each other of state changes by calling each consumer over HTTP.
A producer must know every consumer, a slow consumer adds its latency to the
producer's request, and an unavailable consumer fails it. Three incidents in the
preceding quarter started as one consumer outage and spread to its producers.
Seven services exchange fourteen kinds of state change this way.

## Decision

**Services publish cross-service events to a message bus, and consumers
subscribe to them.** A producer holds no reference to its consumers. Queries
that a service needs answered within a request stay synchronous HTTP.

Rejected: consumers polling a change table in the producer's database. It
couples every consumer to the producer's schema and adds polling load to the
producer's database.

## Consequences

- A consumer outage no longer reaches its producers; events wait on the bus
  until the consumer recovers.
- Consumers see changes after a delay, and must tolerate events that arrive
  more than once or out of order.
- Every service depends on the bus. A bus outage stops all cross-service flows.
- Event payloads become public interfaces. Changing one means coordinating with
  every subscriber.

## Addendum 2026-08-19

The duplicate delivery these Consequences anticipate has occurred in
production. A consumer crashed after sending invoice emails but before
acknowledging the events, received them again on restart, and sent 214 customers
a second invoice email. For a consumer that triggers an external side
effect, duplicate delivery reaches customers. The decision stands.
