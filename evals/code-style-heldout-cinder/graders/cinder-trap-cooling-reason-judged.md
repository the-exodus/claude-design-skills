---
# The cooling comment's 700 degree claim survives only with its reason.
type: llm
focus: { source: file, path: src/controller.rs }
---
Find the comment in `Firing::run_window` just above the duty calculation. The original read:

> The same duty calculation serves cooling segments. It keeps the relay off above about 700 °C, because the kiln sheds heat faster than any rate a schedule asks for, and fires the elements below that to slow the fall.

Nothing in the code mentions 700 °C. "It keeps the relay off above about 700 °C" is true only because of the physical reason in the "because" clause; on its own it reads as a threshold in the code, which is false.

PASS if the comment survives and either keeps the reason (the kiln sheds or loses heat faster than any scheduled cooling rate, in any wording) together with any claim about 700 °C, or drops the 700 °C claim along with the reason while what remains is still true of the code.
FAIL if the comment still says the relay stays off above about 700 °C (or names any temperature threshold) without the physical reason, or if the comment has been removed entirely.
