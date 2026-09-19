---
type: llm
focus: { source: file, path: output.md }
---

This is the list of files created during a task: one new decision record, named NNNN-kebab-case-title.md, where the file name is the record's title.

The decision recorded was: when a tide gauge does not answer, retry three times with a doubling delay, then mark the station silent rather than keep retrying.

PASS if the file name states that decision, in any wording: it says what is done, such as retrying a bounded number of times, giving up, or marking the station silent.
FAIL if the file name names only the topic, such as "retries", "retry-policy", "gauge-retry-approach" or "handling-unresponsive-gauges", without saying what was decided.
FAIL if no file beginning with 0005- is listed.
