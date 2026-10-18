---
# Under-commenting. The one non-local fact, that the first frame after waking repeats the weight from before the scale slept, is said in scale.py, in a comment, a docstring or a name. Matched on its meaning.
type: regex
target: { source: file, path: roastlog/scale.py }
pattern: '(wak|sleep|slept|stale|repeat|previous weight|last weight|power.?sav)'
flags: i
---
