---
# Asked to stop after triage: no source file is edited by the session.
type: regex
target: trace
pattern: '"name":"(?:Edit|Write)","input":\{"file_path":"[^"]*/blastplan/'
match: not_contains
---
