---
type: llm
focus: last_message
---

This is a report on consolidating a project lexicon. Judge one thing only: what it says about the sentence from the old "pickup window" entry, "The window starts when the item is checked in at the pickup branch, not when the patron is notified."

PASS if the report keeps that statement in the rewritten pickup window entry, or says its content lives in src/holds/hold-manager.ts (a doc comment near lines 26-29).
PASS if the report does not mention where that sentence went at all but the consolidated pickup window entry shown in the report still says the window starts at check-in.
FAIL if the report lists that sentence as homeless or as having no other home.
FAIL if the report gives src/notifications/notification-queue.ts, or only an ADR, as the place where that sentence lives.
