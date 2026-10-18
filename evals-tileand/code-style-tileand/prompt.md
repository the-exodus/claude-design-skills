---
description: "Audit. A comment pass over Tileand's Hosting code and tests, brought in at run time from a pinned commit and graded against the owner's labels from THE-221: over-deletion and under-deletion apart, and every shrink re-read on its own. Needs a Tileand checkout and locally generated graders; see evals/README.md."
tags: [code-style, audit, tileand]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 120
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Before I hand this part over, tidy up the comments in `src/Tileand.Core/Hosting/` and `tests/Tileand.Tests/Hosting/`: cut what isn't pulling its weight, and leave the rest. Only those two directories; everything else is read-only. Don't change any code, and don't rename anything.

I won't be around to approve changes, so make them directly. When you're done, list what you deleted, what you shortened and why, in a sentence each.
