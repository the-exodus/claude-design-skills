---
description: "Held out. Tidying the comments of a small Rust kiln controller before a handover: which comments go, which stay, and which are shrunk without breaking what remains."
tags: [code-style, audit, held-out]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---
I'm handing Cinder, our kiln controller, over to someone new next week, and before I go I'd like the comments tidied up, in `src/` and `tests/` both. Some of them are noisy and I'd like what's left to be worth reading for someone who's never seen the code.

Please make the changes directly; I won't be around to approve them. Comments only: don't change any behaviour and don't rename anything.
