---
type: llm
focus: { source: file, path: output.md }
---

Ferrybook settles lapsed holds lazily at the start of each operation and never starts a timer or thread; ADR-0003 decides this deliberately.
PASS if the report does not ask for a timer, a background thread or eager expiry as a fix. Mentioning lazy settlement as deliberate, as checked and sound, or as a rejected finding is a PASS. Reporting that a particular operation fails to settle first (such as confirm) is a different finding and is a PASS.
FAIL if the report presents the absence of a timer or background expiry itself as a defect to fix.
