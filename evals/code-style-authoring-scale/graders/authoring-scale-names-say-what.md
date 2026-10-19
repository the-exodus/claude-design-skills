---
# Naming. The functions, classes and constants the run introduced in scale.py are named for what they are or do.
type: llm
focus: { source: file, path: roastlog/scale.py }
---

This is a Python module an assistant wrote from scratch. It reads a bench scale's serial frames and returns the next stable weight in grams. Judge one thing only: the names of the functions, classes, module-level constants and parameters it introduces. Local variables inside a function body are out of scope, and so is anything imported.

A good name says what the thing is or what it does, in words a reader of the calling code would understand without opening the definition: `next_stable_grams`, `parse_frame`, `Frame`, `WAKE_FRAMES_TO_SKIP`.

PASS if every such name says what the thing is or does.

FAIL if any such name is vague (`Manager`, `Helper`, `Util`, `handle`, `process`, `do_read`, `data`, `info`), names its type rather than its meaning (`frame_str`, `weight_float`, `ScaleClass`), or names how it is implemented rather than what it gives the caller (`loop_until_st`, `regex_frame`). Name the offending identifier in your reasoning.
