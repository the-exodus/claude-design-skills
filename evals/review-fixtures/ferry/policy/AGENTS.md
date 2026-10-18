# Ferrybook

Bookings, fares and the timetable for a small car-ferry operator. Python 3.11+, standard library only.

- Run the tests from the repository root: `python3 -m unittest`
- There is no issue tracker. Work is described in the brief given with the request.
- Money is integer øre everywhere (ADR-0002). Decisions are in `docs/adr/`, superseded and never edited. What the design assumes about Python and the host is in `docs/design/assumptions.md`.
- The base branch is `trunk`.
- A change does only what its brief asks. A defect found outside the brief's scope, however small, is never fixed in the same change: list it in the review report as a follow-up, with its evidence, for the maintainers to schedule.
