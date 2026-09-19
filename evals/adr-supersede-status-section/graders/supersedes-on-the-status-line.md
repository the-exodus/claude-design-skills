---
# The header grammar in references/format.md: the status line is one line, fields separated by a middle dot. Some runs put **Supersedes:** on a line of its own.
type: regex
target: { source: file, path: docs/adr/0005-subscribe-to-gauge-readings-over-mqtt-instead-of-polling.md }
pattern: '^\*\*Status:\*\*[^\n]*\*\*Supersedes:\*\* \[ADR-0002\]\('
flags: m
---
