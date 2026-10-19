---
type: llm
focus: { source: file, path: output.md }
---

This is a Java class after an assistant was asked to tidy a project's comments. Judge one comment only: the Javadoc on `public boolean onCodeScanned(CompartmentId id, String code)`. Before the tidy it read:

> A collection code was scanned at the bank; it is compared with the compartment's code in constant time, since anyone standing at the bank can time the scanner's beep. Returns whether the door was released.

The right change cuts "A collection code was scanned at the bank", which the method's name says. That leaves "it is compared…", whose "it" referred to the code in the cut clause, so a correct shrink repairs the reference ("The scanned code is compared…", "The code is compared…").

Read the comment as it is now, on its own, as a reader who has not seen the original would.

PASS if the comment is still there, every pronoun or "the X" in it has a referent in what remains, it still says the comparison is in constant time and why (anyone at the bank can time the beep), and it claims nothing the original did not. Whether the opening clause was cut is judged elsewhere; a comment left whole passes this check.

FAIL if the comment is gone, if it begins with or contains an "it" (or similar) whose referent is no longer in the comment, if the constant-time reason is lost, or if it adds a claim. Quote the comment as it is now in your reasoning.
