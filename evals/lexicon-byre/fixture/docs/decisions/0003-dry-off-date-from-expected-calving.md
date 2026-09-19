# 0003. The due dry-off date is counted back from expected calving

## Status

Accepted, April 2023.

## Context

Byre used to prompt for dry off at 305 days in milk. That suits a cow who
holds to her first service and nobody else. A cow who took four services was
prompted months before she needed to be, and the herd manager kept a second
list on paper with the real dates, worked out from the services.

What decides when a cow should be dried off is when she will calve, not how
long she has been milking.

## Decision

`LactationService` works out each cow's due dry-off date by counting the
target dry period back from her expected calving date. The expected calving
date is the date of her last service plus the farm's gestation length.

Days in milk no longer play any part in the dry-off list.

## Consequences

- A cow with no service on record has no expected calving date. She never
  reaches the dry-off list and has to be dried off by hand.
- Farms that run a bull with the herd must record the services they see, or
  enter a service date from the vet's pregnancy diagnosis, to get a dry-off
  list at all.
- When a cow is served again, her due dry-off date moves. The list is
  rebuilt from the records every time, so nothing has to be corrected.
- The second paper list has gone.
