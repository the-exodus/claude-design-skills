---
type: llm
focus: { source: file, path: output.md }
---
Find the doc comment on the `Cone` enum. The original read:

> A cone a preset can fire to: 06, 04, 5, 6 or 10. Cones are an enum rather than plain numbers so that a preset cannot name a cone with no known peak: `peak` matches every variant, so a cone added without its temperature fails to compile.

The list "06, 04, 5, 6 or 10" repeats the variants declared directly below and the match in `peak`, and goes stale when a cone is added. The rationale (why an enum, and that the exhaustive match in `peak` turns a missing peak into a compile error) lives nowhere else.

PASS if the list of cone numbers is gone, the rationale survives in substance, and what remains reads as complete sentences on its own: no dangling colon, no "these" or "they" whose referent was the cut list, nothing claiming the code does something it does not.
FAIL if the list of cones is still present, if the rationale is gone or changed in meaning, or if a surviving sentence is broken or refers to the removed list.
