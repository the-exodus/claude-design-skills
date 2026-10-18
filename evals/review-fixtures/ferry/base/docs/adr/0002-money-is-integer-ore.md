# ADR-0002: Money is integer øre

**Status:** Accepted

## Context

Fares were once computed in floating-point kroner, and a season's settlement with the port authority was off by several kroner from rounding.

## Decision

Every amount is an `int` in øre. Percentages and fractions are applied with integer arithmetic (`amount * percent // 100`), never by multiplying by a float. Rejected: `decimal.Decimal`, because nothing here needs more than integer øre and it would spread through every signature.

## Consequences

Division rounds down, in the passenger's favour. Any float in a money calculation is a defect.
