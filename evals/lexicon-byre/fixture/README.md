# Byre

Byre keeps the herd records for a dairy farm. It is the book the herd manager
used to carry in a jacket pocket, plus the arithmetic that book never did.

## What it does

- **A record for every animal.** Ear tag, name, date of birth, sex, parity and
  the management group she is in today. Heifers and cows are told apart: a
  heifer has not calved yet, and several lists treat her differently.
- **Milkings.** Every milking comes in from the parlour meters with the cow's
  ear tag, the time and the yield in kilograms. Milkings add up to a session,
  and sessions to the daily yield.
- **The lactation cycle.** Calving opens a lactation; days in milk count up
  from there. Each service is recorded, the last one gives the expected
  calving date, and from that Byre works out when the cow is due to be dried
  off. Dry off ends the lactation and starts the dry period.
- **Treatments and withdrawal.** Each treatment is recorded with its milk
  withdrawal and its meat withdrawal, as the vet or the data sheet gives them.
  Every cow with an open milk withdrawal is on the withhold list before the
  session opens, and none of her milk is counted as saleable until the
  withdrawal has ended. An animal with an open meat withdrawal is marked as
  not saleable on the cull list.
- **Management groups.** Milkers, dry cows, close-up cows, heifers and any
  other group the farm defines. Byre suggests a move when a cow is dried off,
  comes within the close-up window, or calves; the herd manager confirms it.
- **The daily lists.** Withhold, dry-off, calving, serve and cull. They are
  what the herd manager prints before the morning session.

## Documentation

- [Glossary](docs/glossary.md): the words we use, in the office and in the code.
- [Configuration, lists and reports](docs/configuration.md): every setting in
  `byre.yaml`, and what each list and report shows.
- [Decisions](docs/decisions/README.md): why some things are the way they are.
- [Code conventions](docs/conventions.md).

## Running it

    go build ./cmd/byre
    ./byre -config byre.yaml serve      # meter feed and web pages on :8420
    ./byre -config byre.yaml lists      # print today's lists and exit

Byre keeps everything in one SQLite file beside `byre.yaml`. Back that file up.
There are no accounts: every user on the farm's network sees the same pages.

## Layout

    cmd/byre              entry point
    internal/env          settings, clock, database handle
    internal/herd         animals, the herd store, management groups
    internal/milking      sessions, milkings, the meter feed
    internal/lactation    calving, dry off, the dry period, services
    internal/treatment    treatments and withdrawal
    internal/lists        the daily lists
