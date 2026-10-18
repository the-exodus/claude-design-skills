# blastplan

Plans the blasts at Cold Ash quarry: when each blast may fire, how far apart
blasts must be, whether the predicted ground vibration is within the planning
limit, and the notices sent to neighbours before a blast.

- Python 3.10+, standard library only. Run the tests from this directory with
  `python3 -m unittest`.
- Decisions are recorded in `docs/adr/`; assumptions about things outside the
  code are in `docs/design/assumptions.md`.
- Times are aware UTC datetimes everywhere below `cli.py` (ADR 0001), and the
  clock is passed in (ADR 0004).
- There is no issue tracker. Work is described in the brief given with the
  request.
