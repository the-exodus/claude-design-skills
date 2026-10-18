# ADR-0001: The controller reaches couriers only through the bank

**Status:** Accepted (2026-01-12)

## Context

The lock-board controller runs on the board's own thread, and the courier API
is slow and sometimes down.

## Decision

`CompartmentController` never calls the courier API. It reports to the bank
through `BankListener`, and the bank decides what couriers are told.

## Consequences

A courier API outage cannot stall the lock board.
