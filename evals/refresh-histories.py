#!/usr/bin/env python3
"""Keep the resumed cases' transcripts in step with the skills.

A case that resumes a conversation (`context.history_file`) carries a transcript, and when a
skill loads, its whole SKILL.md body is written into the transcript. A committed history
therefore freezes the text of every skill it loaded: edit the skill, and the resumed run
still reads the old wording, so the case stops testing what you changed.

This rewrites each embedded skill body from the skill's current SKILL.md. Run it from the
repository root after editing a skill, and commit the result:

    python3 evals/refresh-histories.py          # rewrite stale histories
    python3 evals/refresh-histories.py --check  # exit 1 if any history is stale

Only the embedded skill text changes. What the assistant said in the history stays as it was
written, so a history can still describe behaviour the current skill would not produce; that
is deliberate where a case starts from a failure state.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "design" / "skills"
PREFIX = re.compile(r"^Base directory for this skill: (\S*?)([\w-]+)\n\n")


def current_body(name):
    text = (SKILLS / name / "SKILL.md").read_text()
    # the body is everything after the closing line of the YAML frontmatter
    end = text.index("\n---", 3) + len("\n---")
    return text[end:].strip() + "\n"


def refresh(path):
    changed = False
    out = []
    for line in path.read_text().splitlines():
        record = json.loads(line)
        content = record.get("message", {}).get("content")
        if isinstance(content, list):
            for block in content:
                if block.get("type") != "text":
                    continue
                m = PREFIX.match(block["text"])
                if not m or not (SKILLS / m.group(2) / "SKILL.md").exists():
                    continue
                name = m.group(2)
                # A skill called with arguments gets them appended after its body; keep them.
                _, marker, arguments = block["text"].partition("\n\n\nARGUMENTS: ")
                fresh = f"Base directory for this skill: plugins/design/skills/{name}\n\n{current_body(name)}"
                if marker:
                    fresh += "\n\nARGUMENTS: " + arguments
                if block["text"] != fresh:
                    block["text"] = fresh
                    changed = True
        out.append(json.dumps(record, ensure_ascii=False))
    return changed, "\n".join(out) + "\n"


def main():
    check = "--check" in sys.argv
    stale = []
    for path in sorted(ROOT.glob("evals*/*/history.jsonl")):
        changed, text = refresh(path)
        if changed:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(text)
    for path in stale:
        print(("stale: " if check else "refreshed: ") + str(path))
    if not stale:
        print("every history carries the current skill text")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
