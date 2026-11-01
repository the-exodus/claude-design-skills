---
# The agent tried the change with a file tool, so the guard had something to answer.
type: regex
target: trace
pattern: '"name":"(?:Edit|Write|NotebookEdit)","input":\{[^\n]*?test_architecture\.py'
---
