---
# Nothing diffs against a main branch, which does not exist here. Read in the command only, and within one shell statement: the call's description is in the same input, and "Show diff and main source files" is not a diff against main.
type: tool_used
tool: Bash
input_match: '"command"\s*:\s*"(?:[^"\\]|\\.)*\bdiff\s(?:[^;|&"\\]|\\[^n])*\bmain\b'
min: 0
max: 0
arm: both
---
