---
# Over-commenting. No comment or docstring the run added to scale.py only restates what the name, signature and code in view already say.
type: llm
focus: { source: file, path: roastlog/scale.py }
---

This is a Python module an assistant wrote from scratch. It reads a bench scale's serial frames and returns the next stable weight in grams. The scale's protocol document, which is not in view here, says that frames start with `ST` (stable), `US` (settling) or `OL` (overload); that the unit field can be `g` or `kg` and staff may change it at any time; and that the first frame after the scale wakes from power saving is always marked `ST` but repeats the weight shown before it slept.

Judge one thing only: whether the module contains a comment or docstring whose every clause can be read off the code in view: the name it annotates, its signature, or the lines next to it.

A clause carries non-local context, and so is not restatement, when it says something a reader of this file could not see in it: a fact about the scale from the protocol (the wake frame, that the unit may change, what a prefix means when the code does not make it plain), a reason for a non-obvious line, a contract with the caller such as blocking forever or what is raised and when.

PASS if every comment and docstring in the file has at least one clause that carries non-local context, or if the file has no comments at all.

FAIL if any comment or docstring consists only of restatement: for example a docstring on `read_stable_grams` saying "Read a stable weight in grams", a comment `# convert kg to grams` over `if unit == "kg": grams = value * 1000`, or `# split the frame on commas` over `fields = line.split(",")`. Name the comment in your reasoning.
