---
type: llm
focus: { source: file, path: output.md }
---

The branch's confirm(ref) looks the hold up without settling lapsed holds first, so a hold whose time has passed is confirmed if no other operation ran since it lapsed (acceptance criterion 2 broken).
PASS if the report states this defect: confirm can confirm a hold that has already lapsed (because it does not settle or check the deadline first).
FAIL if it does not report it, or reports only that lapsed holds linger in memory without connecting that to confirm.
