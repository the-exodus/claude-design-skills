---
# No Edit or Write is reached before the skill loads. One pattern covers both: a run may edit the file or rewrite it whole.
type: regex
target: trace
pattern: '^(?:(?!"name":"Skill","input":\{"skill":"(?:design:)?design-philosophy")[\s\S])*?"name":"(?:Edit|Write|NotebookEdit)","input"'
match: not_contains
---
