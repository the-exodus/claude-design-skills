# Design fixtures

Invented projects that more than one `design` case runs on. A case's `scaffold.sh` copies one into the workspace, so a fixture here is never in a case's own directory.

- `gaugefeed/`: the gaugefeed river-gauge feed from the `interview-*` cases, grown into a project whose tests run in the eval sandbox with nothing installed. `tests/test_architecture.py` is a stdlib `ast` walk: an allow-list of which gaugefeed modules each module may import (an undeclared module or edge fails), a prohibition on network libraries outside the fetcher, and no import cycles. A rule that a decision drew cites its record, and its failure names the record's path; edges nobody decided cite nothing. ADR-0001 and ADR-0002 are boundaries the tests protect; ADR-0003 (no state between cycles) is a decision no import rule can see. Each boundary was proven by its smallest violation (the report importing the fetcher, the station list importing `urllib`, an undeclared module, a cycle) turning the architecture test red with nothing else failing.

Run its tests from the fixture's root: `python3 -m unittest discover -s tests`.
