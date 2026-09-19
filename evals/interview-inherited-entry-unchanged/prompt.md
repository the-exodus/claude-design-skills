---
description: "A branch closes by deciding how an inherited concept is shown, without changing what the word means. The inherited entry stays as it is."
tags: [interview, lexicon-admission]
plugins: ["../../plugins/design"]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

1. *Stale* keeps meaning exactly what it means: a reading older than two cycles. I don't want the entry touched. What changes is only how a stale reading is drawn: from now on the dashboard shows its age beside the greyed number.
2. Yes. A silent station still shows its last number, greyed, with its age, and a silent marker beside it.
3. It renders as silent until it has made its three in a row. No progress shown.
4. "No reading yet", with no number.
5. A count of silent stations at the top of the board.
6. The moment the state flipped.
7. Two axes. Freshness and aliveness are different things and the board should be able to say "answering, but we only ask hourly".

The rendering is ours too, but keep it out of this interview: design what gaugefeed's output has to carry. Recap and close.
