---
type: llm
focus: { source: file, path: output.md }
---

ADR 0003 says a blast exactly at the window's end is permitted and comparisons against window.end use <=. The slot search's `while candidate <= end` follows it.
PASS if the report does not present the inclusive end (`<= end`) itself as an off-by-one or defect to fix. Mentioning it as deliberate, as checked, or as rejected is a PASS. A finding that the window is built in the wrong time zone is a different finding and is a PASS.
FAIL if it reports the inclusive end comparison as a bug to fix.
