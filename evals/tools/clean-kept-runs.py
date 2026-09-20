#!/usr/bin/env python3
"""Remove the run directories a finished pass kept with --keep-temp, and only those.

    python3 evals/tools/clean-kept-runs.py result.json

A kept run directory (/tmp/claude-eval-XXXX) holds home/ and tmp/ sealed at mode 000, so a
plain rm fails. This opens them first. It removes exactly the directories named by `tracePath`
in the given --json result, so it never touches a run that is still in progress, which a
wildcard would.
"""
import json, os, re, shutil, stat, sys

d = json.load(open(sys.argv[1]))
for case in d["cases"]:
    for r in case["arms"]["with"]:
        m = re.match(r"^/tmp/(claude-eval-[A-Za-z0-9_-]+)/out/trace\.jsonl$", r.get("tracePath") or "")
        if not m:
            continue
        top = "/tmp/" + m.group(1)
        if not os.path.isdir(top):
            continue
        for root, dirs, files in os.walk(top):
            for n in dirs + files:
                p = os.path.join(root, n)
                if not os.path.islink(p):
                    os.chmod(p, os.stat(p).st_mode | stat.S_IRWXU)
        os.chmod(top, os.stat(top).st_mode | stat.S_IRWXU)
        # sealed dirs are mode 000: open them top-down before walking further
        for _ in range(6):
            for root, dirs, files in os.walk(top):
                for n in dirs:
                    p = os.path.join(root, n)
                    if not os.path.islink(p):
                        os.chmod(p, 0o700)
        shutil.rmtree(top)
        print("removed", top)
