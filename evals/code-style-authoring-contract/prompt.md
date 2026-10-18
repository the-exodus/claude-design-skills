---
description: "Authoring. A new public function whose callers must honour a precondition from outside the code: the precondition is in its docstring."
tags: [code-style, authoring]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add a `save(path)` method to `RoastLog` that writes every roast in the log to the SQLite file at `path`, in a table `roasts` with one column per `Roast` field (create the table if it is missing). The office laptop will call it.
