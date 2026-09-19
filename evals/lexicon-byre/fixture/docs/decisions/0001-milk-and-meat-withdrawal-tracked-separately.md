# 0001. Milk and meat withdrawal are tracked separately

## Status

Accepted, June 2022.

## Context

The first version recorded one withdrawal per treatment: a single end date,
and a cow was "under withdrawal" or she was not. That is not how medicines
work. A data sheet gives two figures, one for milk and one for meat, and they
are rarely the same: a few days for milk and several weeks for meat is
common, and some products used on dry cows and youngstock carry a meat
withdrawal and no milk withdrawal at all.

With one end date we had to pick the longer figure. Cows stayed on the
withhold list for weeks after their milk was fit to sell, and milkers learned
to ignore the list.

## Decision

A treatment opens up to two withdrawals, one of kind milk and one of kind
meat, each with its own end. Both run from the last dose of the course, not
the first.

Only a milk withdrawal puts a cow on the withhold list and keeps her milk
out of the saleable total. A meat withdrawal never does; its one effect is to
mark the animal as not saleable on the cull list.

When an animal has several withdrawals of the same kind open, the one that
ends last governs.

## Consequences

- "Is she under withdrawal?" is no longer a yes-or-no question. Every screen
  and list has to say which kind.
- The withhold list got short enough to be believed again.
- Bulls, heifers and calves can carry a meat withdrawal without Byre ever
  looking for their milk.
- The medicine record shows two end dates per treatment.
