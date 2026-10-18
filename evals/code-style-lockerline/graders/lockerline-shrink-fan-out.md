---
# The surviving class comment on FanOutListener stays a why and does not become a false what.
type: llm
focus: { source: file, path: src/lockerline/FanOutListener.java }
---

This is a Java class after an assistant was asked to tidy a project's comments. Judge one comment only: the Javadoc on `FanOutListener`, a listener that forwards each call to every listener it was constructed with. Before the tidy it read:

> Forwards each event to several listeners; used to mirror the bank's events to the support console while an engineer is attached.

The right change cuts "Forwards each event to several listeners", which the class's name and its constructor say, and keeps what the class is used for: mirroring the bank's events to the support console while an engineer is attached.

The trap: the class knows nothing of a support console. It forwards to whatever listeners it is given. "Used to mirror … to the support console" is true, as a statement of purpose. "Mirrors the bank's events to the support console", stated as what the class does, is false.

PASS if the comment is still there and says what the class is used for (or keeps the original whole), and nothing in it states as the class's own behaviour that it writes to, knows of, or talks to a support console.

FAIL if the comment is gone, or if it now describes mirroring to the support console as what the class does rather than what it is used for, or adds a claim the original did not make. Quote the comment as it is now in your reasoning.
