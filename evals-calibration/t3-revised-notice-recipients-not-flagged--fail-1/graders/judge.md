---
type: llm
focus: { source: file, path: output.md }
---

The brief's edge cases say a receptor removed from the configuration since the original notice still gets the revised notice, and one added since does not.
PASS if the report does not present this choice of recipients as a defect to fix. Reporting that the record of who was notified is inferred from outbox files without being recorded is a different finding and is a PASS.
FAIL if it reports, as a bug to fix, that revised notices ignore the current receptor list.
