---
type: llm
focus: { source: file, path: output.md }
---

This is a pytest file an assistant wrote from scratch, testing a function `development_ratio(roast)` that returns the development ratio of a coffee roast as a whole percent, floored rather than rounded (the roaster's own screen floors and people compare the printed report with it), or `None` when first crack or drop is missing.

Judge one thing only: whether the file contains a comment or docstring whose every clause can be read off what is in view: the test's own name, its body and asserts, or the helper it calls.

A clause is not restatement when it says something a reader of the test could not see in it: why a particular value is a good probe (that 19.9 is the case where rounding and flooring disagree, say), what a fixture stands in for, or a fact from outside the test.

PASS if every comment and docstring in the file has at least one such clause, or if the file has no comments at all.

FAIL if any comment or docstring consists only of restatement: for example a docstring on `test_floors_rather_than_rounds` saying "Check that the ratio is floored, not rounded", or a comment `# missing first crack gives None` over `assert development_ratio(r) is None`. Name the comment in your reasoning.
