# Expected verdicts: Tileand's lexicon

Generated from the owner's gold labels by `gen-graders.py`, which lives with the labels
outside this repository. Regenerate rather than edit. Only verdicts are here: Tileand's
entry texts and the owner's reasons stay on the private side, so this repository never
holds Tileand's lexicon and cannot go stale against it.

Input: `docs/design/lexicon.md` at Tileand `3bdb64f`, the commit just before Tileand's own
consolidation (`6163cf3`). That consolidation is a skill run's proposal as corrected
by the owner, so a verdict counts as gold only where the owner marked it, or agreed by
default for the entries no tuning run or judge ever disputed.

| Entry | Verdict | Source |
|---|---|---|
| desired state | rewrite | owner agrees with Tileand's own consolidation |
| actual state | rewrite | owner agrees with Tileand's own consolidation |
| batch | retire | owner agrees with Tileand's own consolidation |
| hold | retire | owner DISAGREES with Tileand's own consolidation |
| track | retire | owner agrees with Tileand's own consolidation |
| emergency show | reframe -> rescue | owner agrees with Tileand's own consolidation |
| session-end show | retire | owner agrees with Tileand's own consolidation |
| gather | rewrite | owner agrees with Tileand's own consolidation |
| fake | retire | owner agrees with Tileand's own consolidation |
| message | rewrite | owner agrees with Tileand's own consolidation |
| request | rewrite | owner agrees with Tileand's own consolidation |
| reply | rewrite | owner agrees with Tileand's own consolidation |
| query | rewrite | owner agrees with Tileand's own consolidation |
| spine | retire | owner agrees with Tileand's own consolidation |
| floor | keep | owner agrees with Tileand's own consolidation |
| layout tree | retire | owner agrees with Tileand's own consolidation |
| ownership tree | retire | owner agrees with Tileand's own consolidation |
| host window | reframe -> window | owner agrees with Tileand's own consolidation |
| ghost | keep the term | owner agrees with Tileand's own consolidation |
| veil | keep the term | owner agrees with Tileand's own consolidation |
| restack | retire | owner agrees with Tileand's own consolidation |
| role | rewrite | owner DISAGREES with Tileand's own consolidation |
| default rules | rename -> shipped defaults | owner DISAGREES with Tileand's own consolidation |
| layout module | reframe -> layout | owner agrees with Tileand's own consolidation |
| LayoutReconciler | reframe -> reconcile | owner agrees with Tileand's own consolidation |
| registry | retire | owner agrees with Tileand's own consolidation |
| curve | rewrite | owner agrees with Tileand's own consolidation |
| border surface | retire | owner agrees with Tileand's own consolidation |
| workspace | rewrite | owner agrees with Tileand's own consolidation |
| animator | retire | agreed by default |
| border look | retire | agreed by default |
| end request | retire | agreed by default |
| facade | retire | agreed by default |
| feature query | retire | agreed by default |
| hidden snapshot | retire | agreed by default |
| Input | retire | agreed by default |
| interop layer | retire | agreed by default |
| Windowing | retire | agreed by default |
| attempt schedule | rewrite | agreed by default |
| compat library | rewrite | agreed by default |
| decoration | rewrite | agreed by default |
| follow | rewrite | agreed by default |
| forced float | keep | agreed by default |
| involuntary end | rewrite | agreed by default |
| membership | rewrite | agreed by default |
| move | rewrite | agreed by default |
| owner | keep | agreed by default |
| promotion | rewrite | agreed by default |
| protocol version | rewrite | agreed by default |
| relinquished | rewrite | agreed by default |
| ring | rewrite | agreed by default |
| root | rewrite | agreed by default |
| satellite | rewrite | agreed by default |
| scratch workspace | rewrite | agreed by default |
| session end | rewrite | agreed by default |
| stack | rewrite | agreed by default |
| switch | rewrite | agreed by default |
| user float | rewrite | agreed by default |
| voluntary end | rewrite | agreed by default |
| warp | rewrite | agreed by default |

Left out of the gold set, never graded: probe, focused member, has the keyboard, user override.

Gaps the owner admitted himself: window, master, successor. A run that proposes them is right; a run
that does not is not penalised, since gap proposals varied a lot between tuning runs.

## What the graders check

`gone-*` and `kept-*`: one per row above, on the written lexicon's entry headings. A
reframe, merge or rename counts as gone for the old headword. Beyond those:
`reframed-rescue`, `reframed-layout`, `reframed-reconcile`, `reframed-shipped-defaults`, `reframed-window` (the word a reframe
or rename lands on is an entry), `redirect-rewritten-default-rules`, `role-rewritten` (fails while the old text stands
word for word), `workspace-behaviour-cut`, `stack-keeps-not-lifo`,
`curve-records-easing`, `no-entry-over-80-words`, `header-admission-replaced`,
`header-exclusion-dropped`, and `skill-fired`.

Tileand's own consolidated lexicon fails only the graders of the rows marked DISAGREES
above, since those are where the owner's label parts from it. `test-graders.py`, beside the
labels, checks exactly that after every regeneration.

Not graded: the report (drift, homeless content, outside edges). Nobody has established
ground truth for those on Tileand.
