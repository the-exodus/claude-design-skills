---
# The guard's message came back to the agent in a tool result. Headless, the hook's ask is a denial and its reason is the tool result.
type: regex
target: trace
pattern: '^(?=[^\n]*"tool_result")[^\n]*tests/test_architecture\.py is protected by this repository''s guard'
flags: m
---
