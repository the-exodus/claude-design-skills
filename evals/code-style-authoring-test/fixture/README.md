# Roastlog

Roastlog keeps the roastery's log: one record per roast, with the green coffee
that went in, the roasted weight that came out, and the times the roaster calls
out. See `docs/lexicon.md` for what the words mean here.

    python -m roastlog report 2026-10-14

The bench scale is a Kessler KB-30 on `/dev/ttyUSB0`; its serial protocol is in
`docs/kb30-protocol.md`.
