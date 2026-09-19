# 2. Cap overdue fines per loan

Date: 2023-06-02

## Status

Accepted

## Context

Fines on long-lost items grew without limit and patrons with a large balance
stopped using the library rather than pay. Staff were already waiving most
fines above ten dollars by hand.

## Decision

A loan's fine stops growing once it reaches `fines.capCents` (default 1000).
The loan moves from the accruing state to a capped state and stays overdue
until the item is returned. Staff may still waive a fine, which moves the loan
to a waived state.

## Consequences

- An overdue loan no longer necessarily accrues a fine: it may be accruing,
  capped or waived.
- Reports on overdue loans must show which of the three states each loan is in.
