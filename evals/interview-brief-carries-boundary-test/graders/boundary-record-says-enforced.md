---
# The record of U1's decision draws a boundary that the architecture test protects, so design:adr's fixed sentence is in it. The file name is the skill's to choose, so this reads the Write of a new record in the trace; the trace also holds the skill's own text, which this pattern does not match.
type: regex
target: trace
pattern: '"name":"Write","input":\{"file_path":"[^"]*docs/adr/000[4-9]-[^"]*","content":"(?:[^"\\]|\\.)*The architecture tests enforce this boundary\.'
---
