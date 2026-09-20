#!/usr/bin/env python3
"""Summarise a run's --json result: one line per run, and under it the graders that failed.

    claude plugin eval . ... --json result.json
    python3 evals/tools/show-run.py result.json

Look at the `error` field before trusting a score. A run that hit a usage or rate limit ends
with that error, is graded on what it produced and usually scores 0, and the suite still
finishes without being marked partial, so it reads like a regression.

A case missing from the output failed to load: the runner says why on stderr, above the table.
"""
import json
import sys

d = json.load(open(sys.argv[1]))
print("reported cost", round(d.get("costUsd", 0), 2), "USD, duration", d.get("durationSeconds"), "s")
for case in d["cases"]:
    for i, r in enumerate(case["arms"]["with"], 1):
        keep = {k: v for k, v in r.items() if k in ("score", "passed", "turns", "durationSeconds", "error", "tracePath")}
        keep["score"] = round(keep["score"], 3)
        print(case["name"], "run", i, keep)
        for g in r["graders"]:
            if not g.get("passed"):
                print("  FAILED:", g["name"], "|", (g.get("explanation") or "")[:500])
