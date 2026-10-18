Everything else for the cycle is ready, but I'm missing the one input I can't supply myself, so I've stopped before launching reviewers.

**What I gathered:**
- Base: `origin/trunk` (confirmed via `refs/remotes/origin/HEAD`, and `AGENTS.md` names `trunk` too)
- Change: 6 files, +211/−19 — `ferrybook/booking.py`, `ferrybook/holds.py`, `ferrybook/pricing.py`, `defaults.json`, plus `tests/test_holds.py` and `tests/test_booking.py`
- Context for reviewers: tests run with `python3 -m unittest` from the root; money is integer øre (ADR-0002); decisions in `docs/adr/` (ADR-0003 *Holds and expiry are settled lazily* looks directly touched); assumptions in `docs/design/assumptions.md`

**What I need: the brief.** `AGENTS.md` says there's no issue tracker and that work is described in the brief given with the request — and no brief came with this one. There's no brief file in `docs/` either. I won't reconstruct it from the commits, the diff, or the branch name: design parity and the adversarial lens both check the change *against* what was asked, so a brief reverse-engineered from the code would let every "the code does X" finding pass by construction, and would make the reviewers blind to exactly what this step exists to catch — behaviour the brief never asked for, and criteria the change missed.

Paste the brief for the seat-holds work — the behaviour wanted, its acceptance criteria, and any edge cases or corrections that came up while it was specified. Then I'll run:

- **Adversarial** and **design parity** (a feature touching a contract other code relies on)
- **Simplification** — the change adds interface surface (new `holds.py` entry points, a new `defaults.json` key)
- **Platform reality** — only if the change touches something `docs/design/assumptions.md` covers; I'll check that against the brief rather than guessing now

If the brief only ever existed as our spoken-out-loud intent, say so and tell me the acceptance criteria as you understand them — that's a usable brief, and I'll note in the report that it was stated at review time rather than before the work.
