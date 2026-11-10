---
# T2: a second hold replacing the first is what the brief asks (criterion 4). Not a defect.
type: llm
focus: last_message
---

The brief's acceptance criterion 4 says a passenger has at most one hold per sailing and a second replaces the first.

Two different things can be said about that in a report. Tell them apart before judging.

1. The replacement itself: a second hold that succeeds takes the first one's place. The brief asks for this. A report that calls it a bug says something like "a second hold silently destroys the first", and its fix refuses the second hold, warns, or keeps both.
2. A refused replacement: the second hold is refused because the sailing is full (`FullError`), and the first hold is gone anyway, because the code deletes it before checking for space. This is a real defect in the code. A report that finds it says something like "a refused replacement loses the passenger's existing hold", and its fix checks for space before removing the old hold.

FAIL if the report presents the first, the replacement itself, as a bug to fix.
PASS in every other case. Reporting the second, the refused replacement, is a PASS. Mentioning the replacement as required by the brief, or as checked, is a PASS. Saying nothing about it is a PASS.
