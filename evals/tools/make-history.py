#!/usr/bin/env python3
"""Turn a kept run's stored session into a clean history.jsonl for a resumed case.

    python3 evals/tools/make-history.py <stored session .jsonl> <out history.jsonl>
        [--drop-skill NAME]... [--cwd /work/project]

A case resumes a conversation with `context.history_file` in its case.yaml. The most faithful
source for one is the runner itself: run a case with --keep-temp, and the run's real session is
under /tmp/claude-eval-XXXX/config/projects/<cwd>/<session>.jsonl (open the kept directory first:
chmod 700 on it and on its sealed/). A resumed run saves no such file; grow its history with
extend-history.py instead.

This keeps only the conversation: user and assistant records, in order, re-linked into one
chain by uuid and parentUuid, which is all a history needs. It drops thinking blocks, harness
bookkeeping and environment attachments, reads of the plugin's own files (a machine path, and
text that would go stale), and every trace of the run's temp directory. With --drop-skill it
also drops the records of that skill loading, so the history reads as a session in which it
has not loaded yet.

The skill text that a load embeds stays in, and goes stale when the skill changes: run
evals/refresh-histories.py afterwards, and again after every edit to a skill.
"""
import json
import re
import sys
import uuid

args = sys.argv[1:]
src, out = args[0], args[1]
drop = [args[i + 1] for i, a in enumerate(args) if a == "--drop-skill"]
cwd = next((args[i + 1] for i, a in enumerate(args) if a == "--cwd"), "/work/project")

SESSION = "00000000-0000-4000-8000-000000000001"
records = [json.loads(line) for line in open(src)]
records = [r for r in records if r.get("type") in ("user", "assistant") and not r.get("isSidechain")]

dropped_tool_ids, kept = set(), []
for r in records:
    m = r["message"]
    c = m.get("content")
    if isinstance(c, list):
        c = [b for b in c if b.get("type") not in ("thinking", "redacted_thinking")]
        if not c:
            continue
        uses = [b for b in c if b.get("type") == "tool_use"]
        if any(b["name"] == "Skill" and any(b["input"].get("skill", "").endswith(d) for d in drop) for b in uses):
            dropped_tool_ids.update(b["id"] for b in uses)
            continue
        if any(b["name"] in ("Read", "Glob", "Grep") and re.search(r"/plugins/design/|/skills/", json.dumps(b["input"])) for b in uses):
            dropped_tool_ids.update(b["id"] for b in uses)
            continue
        if any(b.get("type") == "tool_result" and b.get("tool_use_id") in dropped_tool_ids for b in c):
            continue
        if r.get("isMeta") and r.get("sourceToolUseID") in dropped_tool_ids:
            continue
        m = {**m, "content": c}
    rec = {"type": r["type"], "isSidechain": False, "sessionId": SESSION, "version": r.get("version", "2.1.278"),
           "cwd": cwd, "userType": "external", "timestamp": r["timestamp"], "message": m}
    for k in ("isMeta", "sourceToolUseID", "toolUseResult"):
        if k in r:
            rec[k] = r[k]
    if r["type"] == "assistant":
        rec["message"] = {k: v for k, v in m.items() if k in ("id", "type", "role", "model", "content", "stop_reason", "stop_sequence")}
        rec["message"]["usage"] = {"input_tokens": 0, "output_tokens": 0}
    kept.append(rec)

prev = None
for n, rec in enumerate(kept):
    rec["uuid"] = str(uuid.UUID(int=(1 << 64) + n))
    rec["parentUuid"] = prev
    prev = rec["uuid"]

text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kept)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+/home/cwd", cwd, text)
# A skill's base directory is machine-specific; refresh-histories.py rewrites these records anyway.
text = re.sub(r"Base directory for this skill: [^\\\"]*?/skills/", "Base directory for this skill: plugins/design/skills/", text)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+/home", "/work", text)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+", "/work", text)
left = [text[max(0, m.start() - 60):m.end() + 60] for m in re.finditer(r"/home/|claude-eval", text)]
if left:
    sys.exit("machine-specific path left in the history, fix the tool before committing it: " + repr(left[:3]))
open(out, "w").write(text)
print(len(kept), "records,", len(text), "bytes ->", out)
