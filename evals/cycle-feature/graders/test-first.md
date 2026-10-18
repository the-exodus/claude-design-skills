---
# No fix to ferrybook/ is written before the first test is written (test-first fixes). One pattern covers Edit and Write.
type: regex
target: trace
pattern: '^(?:(?!"name":"(?:Edit|Write)","input":\{"file_path":"[^"]*/tests/)[\s\S])*?"name":"(?:Edit|Write)","input":\{"file_path":"[^"]*/ferrybook/'
match: not_contains
---
