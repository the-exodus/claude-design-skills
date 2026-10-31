---
# The open fork, what a station that missed the previous cycle is compared against, is a provisional item: a line that starts with its P id asks it.
type: regex
target: { source: file, path: batch.md }
pattern: '(?:^|\n)[#*\s-]*P\d\b[^\n]{0,300}?(?:did(?:n.t| not) answer|nothing to compare|no previous|without a previous|no (?:earlier|prior|last|previous) (?:reading|level|cycle)|miss(?:ed|es|ing)? (?:the |a |one |its )?(?:previous |last |prior )?(?:cycle|reading)|absent|unanswered|silent|went quiet|was down|down last|no baseline|gap|compar\w*|last known|how old|older (?:level|reading)|not (?:in )?(?:the )?(?:last|previous|prior) cycle|\bmissed\b|carr\w* (?:a |the |its )?(?:level|reading) forward)'
flags: i
---
