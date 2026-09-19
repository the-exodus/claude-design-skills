---
# The old ADR records the new status in the field it already has: a **Status:** line.
type: regex
target: { source: file, path: docs/adr/0002-poll-gauges-every-five-minutes.md }
pattern: '^\*\*Status:\*\* Superseded by \[ADR-0005\]\(0005-subscribe-to-gauge-readings-over-mqtt-instead-of-polling\.md\)'
flags: m
---
