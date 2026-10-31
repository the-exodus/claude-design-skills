---
# The open fork, what a station shows when it missed the previous cycle, is a provisional item (after a P id, before the appendix).
type: regex
target: { source: file, path: batch.md }
pattern: '\bP\d\b(?:(?!appendix)[\s\S])*?(?:(?:previous|last|prior|earlier)[^\n]{0,60}(?:cycle|reading)[^\n]{0,120}(?:miss|absent|no reading|didn.t answer|did not answer|unanswered|gap|silent)|(?:miss|absent|no reading|didn.t answer|did not answer|unanswered|silent)[^\n]{0,120}(?:previous|last|prior|earlier) cycle)'
flags: i
---
