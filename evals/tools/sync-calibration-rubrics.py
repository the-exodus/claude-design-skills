#!/usr/bin/env python3
"""Copy each llm grader's rubric from the suite into its calibration cases.

    python3 evals/tools/sync-calibration-rubrics.py          # rewrite the copies that differ
    python3 evals/tools/sync-calibration-rubrics.py --check  # exit 1 if any copy differs

A calibration case (evals-calibration/<grader>--<pass|fail>-<n>/) carries a copy of the rubric
of evals/<case>/graders/<grader>.md, pointed at a fixed output instead of at a run. The copy
has to be the wording the suite uses, or the agreement recorded for the grader describes a
rubric nobody runs. After changing a rubric, run this, then re-run that grader's calibration:

    claude plugin eval . --eval-dir evals-calibration --judge-model claude-opus-5 --ablation none \\
        --scaffold --tag <grader> --runs 5 -j 8 --json calibration.json
    python3 evals-calibration/score.py calibration.json

A grader with no calibration case is reported, since it is an llm grader nobody has checked.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
check = "--check" in sys.argv


def body(path):
    return path.read_text().split("---\n", 2)[2].strip()


suite = {}
for path in sorted(ROOT.glob("evals*/*/graders/*.md")):
    if path.parts[-4] == "evals-calibration":
        continue
    head = path.read_text().split("---\n", 2)[1]
    if "type: llm" in head:
        if path.stem in suite:
            sys.exit(f"two llm graders are both named {path.stem}; calibration cases are keyed by that name")
        suite[path.stem] = path

differ, covered = [], set()
for case in sorted((ROOT / "evals-calibration").glob("*--*")):
    grader = case.name.split("--")[0]
    judge = case / "graders" / "judge.md"
    if grader not in suite:
        print(f"orphan: {case.name} calibrates a grader the suite no longer has")
        continue
    covered.add(grader)
    fresh = body(suite[grader])
    if body(judge) != fresh:
        differ.append(case.name)
        if not check:
            head = judge.read_text().split("---\n", 2)[1]
            judge.write_text(f"---\n{head}---\n\n{fresh}\n")

for name in differ:
    print(("differs: " if check else "synced: ") + name)
for grader in sorted(set(suite) - covered):
    print(f"uncalibrated: {suite[grader].relative_to(ROOT)} has no calibration case")
if not differ:
    print(f"{len(covered)} llm graders, every calibration copy matches the suite")
sys.exit(1 if check and differ else 0)
