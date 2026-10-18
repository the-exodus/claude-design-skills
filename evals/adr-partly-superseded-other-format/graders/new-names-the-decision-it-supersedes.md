---
# The new ADR's status line names the one decision it takes over: **Supersedes:** the <decision> decision in [ADR-0001](...), after a middle dot.
type: regex
target: { source: file, path: docs/adr/0005-replicate-station-write-ahead-logs-continuously-to-object-storage.md }
pattern: '^\*\*Status:\*\*[^\n]*\*\*Supersedes:\*\* the [^\n]*decision in \[ADR-0001\]\(0001-store-readings-in-sqlite-and-back-up-nightly\.md\)'
flags: m
---
