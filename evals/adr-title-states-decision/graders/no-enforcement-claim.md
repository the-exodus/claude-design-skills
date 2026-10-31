---
# A retry policy draws no boundary, so the new record makes no claim that one is enforced. The file name is the skill's to choose, so this reads the Write of record 0005 in the trace; the trace also holds the skill's own text, which this pattern does not match.
type: regex
target: trace
pattern: '"name":"Write","input":\{"file_path":"[^"]*docs/adr/0005-[^"]*","content":"(?:[^"\\]|\\.)*enforce this boundary'
flags: i
match: not_contains
---
