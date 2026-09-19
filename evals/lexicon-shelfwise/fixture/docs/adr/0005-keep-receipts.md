# 5. Keep receipts as records

Date: 2024-01-22

## Status

Accepted

## Context

Until now branches printed a paper due slip at checkout and kept nothing.
Patrons lost the slip, forgot their due dates, and asked staff to look them up.

## Decision

Every checkout and every renewal issues a receipt listing each item and its
due date. Receipts are stored against the patron and can be viewed through
`GET /patrons/{id}/receipts`. Printing is optional.

## Consequences

- Patrons can see past receipts in the app.
- Receipts are kept for two years, then deleted.
