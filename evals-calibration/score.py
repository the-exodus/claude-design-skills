#!/usr/bin/env python3
"""Score a calibration run: how often each llm grader agrees with the known verdict, and whether it flips.

    claude plugin eval . --eval-dir evals-calibration --judge-model claude-opus-5 --ablation none \\
        --scaffold --runs 5 -j 8 --json calibration.json
    python3 evals-calibration/score.py calibration.json

Each case is one fixed output with a known verdict, named <grader>--<pass|fail>-<n>. A grading
is three judge votes, of which two decide. For each grader this reports:

  agreement  gradings whose verdict matched the known one, over all gradings
  flips      fixed outputs that did not get the same verdict on every re-grade
  split      gradings the three votes did not agree on, a quieter sign of noise

The bar (provisional, see evals/README.md): agreement of at least 0.9 and no flips.
"""
import collections
import json
import re
import sys

BAR = 0.9
result = json.load(open(sys.argv[1]))
graders = collections.defaultdict(lambda: {"gradings": 0, "agree": 0, "split": 0, "flipped": [], "wrong": []})

for case in result["cases"]:
    m = re.fullmatch(r"(.+)--(pass|fail)-(\d+)", case["name"])
    if not m:
        continue
    grader, expected = m.group(1), m.group(2) == "pass"
    g = graders[grader]
    verdicts = []
    for run in case["arms"]["with"]:
        if run.get("error"):
            sys.exit(f"{case['name']}: run error, scores are not comparable: {run['error']}")
        judge = run["graders"][0]
        verdicts.append(judge["passed"])
        g["gradings"] += 1
        g["agree"] += judge["passed"] == expected
        votes = re.findall(r"\b(PASS|FAIL)\b", judge.get("explanation") or "")
        g["split"] += len(set(votes)) > 1
    if len(set(verdicts)) > 1:
        g["flipped"].append(case["name"])
    elif verdicts and verdicts[0] != expected:
        g["wrong"].append(case["name"])

print(f"{'grader':42} {'agreement':>10} {'flips':>6} {'split':>6}   verdict")
failed = False
for name, g in sorted(graders.items()):
    agreement = g["agree"] / g["gradings"]
    ok = agreement >= BAR and not g["flipped"]
    failed |= not ok
    print(f"{name:42} {g['agree']:>4}/{g['gradings']:<3} {agreement:4.2f} {len(g['flipped']):>5} {g['split']:>6}   {'meets the bar' if ok else 'BELOW THE BAR'}")
    for case in g["wrong"]:
        print(f"    always wrong: {case}")
    for case in g["flipped"]:
        print(f"    flipped:      {case}")
sys.exit(1 if failed else 0)
