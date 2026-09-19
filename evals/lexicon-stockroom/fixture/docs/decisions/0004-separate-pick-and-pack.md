# 4. Separate picking from packing

## Status

Accepted

## Context

Pickers packed at the shelf, which slowed picking and put packing materials
in every aisle.

## Decision

Pickers only pick. They bring picked goods to the pack benches, where
packers check them against the order, pack them and print the packing slip.

## Consequences

- A pick task ends at the pack bench, not at the dock.
- Packing has its own station and its own staff.
