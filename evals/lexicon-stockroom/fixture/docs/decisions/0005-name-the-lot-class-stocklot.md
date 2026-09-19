# 5. Name the lot class StockLot

## Status

Accepted

## Context

Operators and suppliers call units received together with one expiry date
a batch, and the carton label says "batch number". In the code, "batch"
already names the nightly batch jobs in `jobs.py`.

## Decision

The class is named `StockLot`, and its number field `lot_no`.

## Consequences

- Screens and labels still say "batch number"; only the code says lot.
- Developers have to know that a StockLot is what operators call a batch.
