---
# The assistant says nothing substantial before the skill loads. Only assistant lines count: a loading skill's body arrives as a long text block in a user message. The trace of a resumed run holds only the new messages; a short line announcing the load is fine, 600 characters of prose before it is a tree being seeded or a branch being worked without the principles.
type: regex
target: trace
pattern: '^(?:(?!"name":"Skill","input":\{"skill":"(?:design:)?design-philosophy")[\s\S])*?\{"type":"assistant"[^\n]*?"type":"text","text":"(?:[^"\\]|\\.){600,}'
match: not_contains
---
