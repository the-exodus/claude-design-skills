---
# Nothing added. No comment in LockerBank.java makes a claim its original comments did not.
type: llm
focus: { source: file, path: src/lockerline/LockerBank.java }
---

This is a Java class after an assistant was asked to tidy a project's comments, cutting what was not pulling its weight. Tidying may delete or shorten comments, and may repair a sentence left broken by a cut. It must not add claims. Before the tidy the file's comments were, in order:

1. On the class: "One cabinet at one site. Its state changes only on the bank's own executor, never on the lock-board thread, which is why every listener call is posted to it."
2. Trailing on the `ledger` field: "at most one open reservation per compartment: the ledger's lock holds that, not this class"
3. On `completeDropOff`: "The tail of every drop-off the bank accepts: frees the courier's reservation and logs the drop-off."
4. On `onCodeScanned`: "A collection code was scanned at the bank; it is compared with the compartment's code in constant time, since anyone standing at the bank can time the scanner's beep. Returns whether the door was released."
5. Trailing on `if (failed >= 3) lockOut(id);`: "three tries, as the printed receipt promises"

Judge one thing only: whether any comment in the file now says something none of these said: a new fact, a narrower or wider scope, a reason, a condition, a number, or a new comment where there was none.

PASS if every claim in every comment now in the file was made by one of the originals. Rewording, shortening, and replacing a pronoun with the noun it stood for do not count as adding.

FAIL if any comment states something the originals did not, for example that refused drop-offs keep their reservation, that the lockout lasts until a courier round, that a comparison uses a particular API, or a new comment on a member that had none. Quote the added claim in your reasoning.
