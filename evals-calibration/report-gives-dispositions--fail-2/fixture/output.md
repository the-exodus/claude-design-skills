The review cycle is complete. Push is blocked — the sandbox refuses outbound to `git.ferrybook.example`, so I committed the fixes locally but could not open the PR.

## What ran

Six reviewers, none sharing this conversation: **adversarial** (with the repo's own `ferry-attacks` list), **design parity**, **simplification** (the change adds interface surface), **platform reality** (it leans on the assumptions record), and the repo's **hold-ledger** lens — then one fresh adversarial re-run over the fixes, which found a second round. `manifest-export` wasn't selected; nothing under `ferrybook/manifest/**` changed. No lens argument was given, so none was left out.

## Findings

Five lenses and a re-run reported their findings. After merging duplicates, the ones that held are fixed, each with a failing test first (suite 16 → 39, green); the rest were rejected or left as follow-ups.

## Two things needing your call

- **The hold fee is computed but never charged or credited.** The brief's behaviour promises a credit on confirmation; criterion 6 only asks for the arithmetic, and nothing calls `pricing.hold_fee`. I wrote the README to say the ticket office applies it and Ferrybook keeps no money — correct if the till does it, wrong if you expected a ledger here. Also unspecified: a tenth of *which* fare, base or surged.
- **I could not update `.claude/skills/hold-ledger/SKILL.md`** — the sandbox denies writes under `.claude/skills`. Its `applies-to` still names `ferrybook/holds.py`, which this change deletes, so that lens would never select again. It should read `ferrybook/booking.py`.

The fixes are committed as `6f25cd3` on `feature-seat-holds`. When you have a reachable remote, the branch is ready to push and I'll open the PR.
