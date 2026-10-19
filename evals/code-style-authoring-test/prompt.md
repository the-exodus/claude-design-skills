---
description: "Authoring. Tests for a rule recorded in an ADR, in a project whose convention bars citations in tests: none is written, and no comment restates a test's name or asserts."
tags: [code-style, authoring]
plugins: ["../../plugins/design", "../../plugins/implementation"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add tests for `development_ratio` in `tests/test_development_ratio.py`: that it floors rather than rounds, and that it gives `None` when first crack or drop is missing. Use pytest, like the other tests.
