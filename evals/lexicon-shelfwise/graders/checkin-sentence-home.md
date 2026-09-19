---
type: llm
focus: last_message
---

This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "pickup window" entry, "The window starts when the item is checked in at the pickup branch, not when the patron is notified."

The written lexicon is not shown to you, only the report, so silence about this sentence is not a failure.

FAIL if the report lists that sentence, or its substance (the window starts at check-in rather than at notification), among the homeless content or as having no other home.
FAIL if the report gives src/notifications/notification-queue.ts as a place where that statement lives. This fails even when the report names the true home beside it: that file's doc comment mentions the pickup notices without saying when the window starts, so it is not a home.
PASS in every other case: the report says the statement stays in the entry, or names src/holds/hold-manager.ts as its home, or does not say where it went. Citing notification-queue.ts for other content, such as the notices themselves, does not fail.
