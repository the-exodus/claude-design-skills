---
name: hold-ledger
description: Review lens for Ferrybook's hold handling. Not for ordinary sessions.
disable-model-invocation: true
metadata:
  review-lens:
    applies-to: ["ferrybook/holds.py"]
---

# Hold ledger review

You are a fresh-context reviewer checking one thing: that every hold has exactly one release path. A hold is released by being confirmed, cancelled, expired or replaced, and by nothing else.

## Method

1. Read `git diff` against the base branch, then `ferrybook/holds.py` and every caller of it.
2. For each way a hold comes into being, trace each way it can end. A hold that can end two ways at once (say, expired and confirmed in the same operation) or no way at all is a finding.

## Report

Findings only, each with `file:line`, the path that is missing or doubled, and the smallest fix. Then the paths you traced and found sound. Do not edit any file.
