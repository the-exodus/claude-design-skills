# ADR-0003 — Each cycle is a fresh process that keeps no state

**Status:** Accepted (2025-04-02)

## Context

Gaugefeed runs on the same host as the dashboard, where cron already starts the other jobs. A long-running service would need its own supervision, restarts and logging, none of which the host has for anything else.

## Decision

Cron starts `python -m gaugefeed stations.txt` once per cycle. The process fetches every station, prints the document and exits; nothing it learned is kept for the next cycle, on disk or anywhere else. Each cycle's document stands on its own.

A daemon that polls on its own timer was rejected because it would need supervision the host does not provide, and a hung daemon stops the feed where a hung cron run only loses one cycle. Keeping a state file between cycles was rejected for now because nothing in the document needed it, and a state file brings locking, corruption and clean-up with it.

## Consequences

A crash or a hung cycle costs one cycle and no more; the next starts clean. Gaugefeed knows nothing about earlier cycles when it builds a document.
