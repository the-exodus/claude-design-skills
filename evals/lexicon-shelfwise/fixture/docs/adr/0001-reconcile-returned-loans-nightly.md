# 1. Reconcile returned loans nightly

Date: 2023-04-11

## Status

Accepted

## Context

When a branch loses its connection, staff keep scanning returns on the
terminal and the returns sync to the server once the connection is back,
sometimes a day or more later. The nightly fine run does not know about those
returns yet and keeps charging fines on items that are already back on the
shelf. Patrons have complained about fines for days after they returned an
item.

## Decision

A nightly job, `LoanReconciler`, runs after the fine run. For every loan
returned in the last 24 hours it recomputes the fine owed at the recorded
return time and lowers the stored fine to that amount. The schedule is set by
`reconciler.sweepCron`.

## Consequences

- The fine run and the reconciliation job must run in that order; the default
  schedule places the reconciliation job at 03:00, after the fine run.
- The recorded return time, not the sync time, is authoritative for fines.
