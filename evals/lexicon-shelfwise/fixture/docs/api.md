# Patron API

All endpoints need a signed-in patron. Only members (patrons whose library
card is active) can borrow or place holds; other patrons can still see their
loans and pay fines.

## Loans

`GET /patrons/{id}/loans` lists the patron's loans with their due dates and
any fine.

`POST /loans/{id}/renew` renews a loan: the due date is reset to a full loan
period from today. A loan can be renewed at most `loans.maxRenewals` times,
and not at all while someone has a hold on the title.

`POST /loans/{id}/extend` with `{ "days": n }` extends a loan: the due date
moves back by `n` days. An extension does not count as a renewal and is
allowed even when the title has holds.

A returned item is never still charged: fines stop at the time of return,
even if the return was scanned at a branch that was offline at the time.

## Holds

`POST /holds` with `{ "titleId": ..., "pickupBranchId": ... }` places a hold
on a title. You choose the branch where you want to collect it.

When an item is ready you have `holds.pickupWindowDays` days to collect it at
your pickup branch, or the hold lapses.

## Receipts

`GET /patrons/{id}/receipts` lists the receipts issued at each checkout and
renewal.
