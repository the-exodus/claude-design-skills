---
# Under-commenting. The decision kept out of an ADR has its reason in report.py: rounding down matches what the roaster's screen shows. Matched on its meaning: the screen, the display, or matching what people compare.
type: regex
target: { source: file, path: roastlog/report.py }
pattern: '(screen|display|roaster.{0,30}(shows|reads)|compare|match(es|ing)? the roaster|held? (up )?against)'
flags: i
---
