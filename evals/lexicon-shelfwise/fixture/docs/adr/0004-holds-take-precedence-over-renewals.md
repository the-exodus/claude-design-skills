# 4. Holds take precedence over renewals

Date: 2023-09-05

## Status

Accepted

## Context

Popular titles were renewed again and again by the same patrons while others
waited in the hold queue for months.

## Decision

A loan cannot be renewed while its title has a waiting hold. Extensions are
still allowed, up to `loans.maxExtensionDays`, because they do not restart the
loan period.

## Consequences

- Patrons are told why a renewal was refused and offered an extension.
- A patron can no longer keep a popular title indefinitely.
