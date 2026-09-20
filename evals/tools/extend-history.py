#!/usr/bin/env python3
"""Grow a history by one exchange: the user turn that was sent, and what a resumed run answered.

    python3 evals/tools/extend-history.py <history.jsonl> <prompt file> <run trace.jsonl> <out.jsonl>
        [--drop-skill NAME]... [--text-only [--cut-first-paragraph-matching REGEX]]

A multi-turn history is chained: resume the history so far with the next user turn as the
case's prompt, run once with --keep-temp, then append that turn and the run's answer here. The
trace (/tmp/claude-eval-XXXX/out/trace.jsonl) holds only the run's new messages, in stream
format, which is why the prompt file is needed too.

Thinking blocks are dropped. With --drop-skill, so is every record of that skill loading, so
the result reads as a session in which it still has not loaded. With --text-only, only the
assistant's prose is kept, without tool calls or their results: use it when the turn's tool use
is noise, such as reads of paths that exist only in the run's temp directory.

Run evals/refresh-histories.py on the result, and again after every edit to a skill.
"""
import json
import re
import sys
import uuid

hist_path, prompt_path, trace_path, out = sys.argv[1:5]
drop = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--drop-skill"]
hist = [json.loads(l) for l in open(hist_path)]
base = {k: hist[0][k] for k in ("isSidechain", "sessionId", "version", "cwd", "userType")}
stamp = lambda n: f"2026-09-19T21:{(n // 60) % 60:02d}:{n % 60:02d}.000Z"

new = [{"type": "user", "message": {"role": "user", "content": open(prompt_path).read().strip()}}]
dropped = set()
for line in open(trace_path):
    o = json.loads(line)
    if o.get("type") not in ("assistant", "user"):
        continue
    m = o["message"]
    c = m.get("content")
    if isinstance(c, list):
        c = [b for b in c if b.get("type") not in ("thinking", "redacted_thinking")]
        if not c:
            continue
        uses = [b for b in c if b.get("type") == "tool_use"]
        if any(b["name"] == "Skill" and any(b["input"].get("skill", "").endswith(d) for d in drop) for b in uses):
            dropped.update(b["id"] for b in uses)
            continue
        if any(b.get("type") == "tool_result" and b.get("tool_use_id") in dropped for b in c):
            continue
        if any(b.get("type") == "text" and re.match(r"Base directory for this skill: \S*/(" + "|".join(map(re.escape, drop or ["\0"])) + r")\s", b["text"]) for b in c):
            continue
        if "--text-only" in sys.argv:
            # keep the assistant's prose alone: no tool calls, no results
            if o["type"] != "assistant":
                continue
            c = [b for b in c if b.get("type") == "text" and b["text"].strip()]
            if not c:
                continue
            cut = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--cut-first-paragraph-matching"), None)
            if cut and re.search(cut, c[0]["text"].split("\n\n", 1)[0]):
                c[0] = {**c[0], "text": c[0]["text"].split("\n\n", 1)[1]}
    if o["type"] == "assistant":
        m = {k: v for k, v in m.items() if k in ("id", "type", "role", "model", "stop_reason", "stop_sequence")}
        m["content"] = c
        m["usage"] = {"input_tokens": 0, "output_tokens": 0}
    else:
        m = {"role": "user", "content": c}
    new.append({"type": o["type"], "message": m})

records = hist + [{**base, **r} for r in new]
prev = None
for n, r in enumerate(records):
    # One chain, re-numbered from the top, so a history can be extended any number of times.
    r["uuid"] = str(uuid.UUID(int=(1 << 64) + n))
    r["parentUuid"] = prev
    r.setdefault("timestamp", stamp(n))
    prev = r["uuid"]
text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+/home/cwd", base["cwd"], text)
text = re.sub(r"Base directory for this skill: [^\\\"]*?/skills/", "Base directory for this skill: plugins/design/skills/", text)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+/home", "/work", text)
text = re.sub(r"/tmp/claude-eval-[A-Za-z0-9_-]+", "/work", text)
left = [text[max(0, m.start() - 60):m.end() + 60] for m in re.finditer(r"/home/|claude-eval", text)]
if left:
    sys.exit("machine-specific path left in the history, fix the tool before committing it: " + repr(left[:3]))
open(out, "w").write(text)
print(len(hist), "+", len(new), "records ->", out, "| dropped skill loads:", len(dropped))
