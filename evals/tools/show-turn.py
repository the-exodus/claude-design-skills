#!/usr/bin/env python3
"""Show what a run did, in order, from its kept trace: each tool call, and each thing it said.

    claude plugin eval . ... --keep-temp --json result.json
    python3 evals/tools/show-turn.py /tmp/claude-eval-XXXX/out/trace.jsonl [--full]

The path is each run's `tracePath` in the --json result. Long messages are shown head and
tail unless --full is given.

Read a failure here before believing it. A grader that fails may be wrong about the run rather
than the run being wrong: most failures in this suite's first runs were a pattern that did not
expect how a correct run had phrased something.
"""
import json
import sys

full = "--full" in sys.argv
for i, line in enumerate(open(sys.argv[1]), 1):
    o = json.loads(line)
    if o.get("type") != "assistant":
        continue
    for b in o["message"]["content"]:
        if b["type"] == "tool_use":
            print(i, "TOOL", b["name"], json.dumps(b["input"])[:100])
        elif b["type"] == "text" and b["text"].strip():
            t = b["text"]
            print(i, "TEXT", len(t), "chars")
            print(t if full or len(t) < 2600 else t[:900] + "\n   [...]\n" + t[-1500:])
