---
type: llm
focus: { source: file, path: output.md }
---

This is a Python module of a coffee roastery's log. Before the assistant's change it had no comments or docstrings at all; every comment or docstring in it now was added by the assistant, which was asked to add a development ratio to the day report: development time (first crack to drop) as a share of total roast time (charge to drop), as a whole percent rounded down, with a dash when first crack or drop is missing. The user gave a reason for rounding down that is not visible in the code: the roaster's own screen rounds down and people compare the printed report with it.

Judge one thing only: whether the module contains a comment or docstring whose every clause can be read off the code in view: the name it annotates, its signature, or the lines next to it.

A clause carries non-local context, and so is not restatement, when it says something a reader of this file could not see in it: the reason for rounding down (the roaster's screen), what the domain terms mean where the code does not show it, or a contract with the caller.

PASS if every comment and docstring in the file has at least one clause that carries non-local context, or if the file has no comments at all.

FAIL if any comment or docstring consists only of restatement: for example a docstring on `development_ratio` saying "Return the development ratio", a comment `# no first crack or no drop: dash` over `if roast.first_crack_at is None or roast.dropped_at is None: return "-"`, or `# round down` over `math.floor(...)` with no reason given. Name the comment in your reasoning.
