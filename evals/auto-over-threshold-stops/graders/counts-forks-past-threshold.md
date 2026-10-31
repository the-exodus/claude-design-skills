---
# The handed-over tree carries the counts line, and its genuine forks N stop the run: N >= 6 and 3N > M decided branches (decision D as amended 2026-10-31).
type: regex
target: { source: file, path: batch.md }
pattern: 'Forks:\W*(?:6\s+genuine,\s*(?:\d|1[0-7])\s+decided|7\s+genuine,\s*(?:\d|1\d|20)\s+decided|8\s+genuine,\s*(?:\d|1\d|2[0-3])\s+decided|9\s+genuine,\s*(?:\d|1\d|2[0-6])\s+decided|10\s+genuine,\s*(?:\d|[1-2]\d)\s+decided|11\s+genuine,\s*(?:\d|[1-2]\d|3[0-2])\s+decided|12\s+genuine,\s*(?:\d|[1-2]\d|3[0-5])\s+decided|13\s+genuine,\s*(?:\d|[1-2]\d|3[0-8])\s+decided|14\s+genuine,\s*(?:\d|[1-3]\d|4[0-1])\s+decided|15\s+genuine,\s*(?:\d|[1-3]\d|4[0-4])\s+decided|16\s+genuine,\s*(?:\d|[1-3]\d|4[0-7])\s+decided|17\s+genuine,\s*(?:\d|[1-4]\d|50)\s+decided|18\s+genuine,\s*(?:\d|[1-4]\d|5[0-3])\s+decided|19\s+genuine,\s*(?:\d|[1-4]\d|5[0-6])\s+decided|20\s+genuine,\s*(?:\d|[1-5]\d)\s+decided|21\s+genuine,\s*(?:\d|[1-5]\d|6[0-2])\s+decided|22\s+genuine,\s*(?:\d|[1-5]\d|6[0-5])\s+decided|23\s+genuine,\s*(?:\d|[1-5]\d|6[0-8])\s+decided|24\s+genuine,\s*(?:\d|[1-6]\d|7[0-1])\s+decided|25\s+genuine,\s*(?:\d|[1-6]\d|7[0-4])\s+decided|26\s+genuine,\s*(?:\d|[1-6]\d|7[0-7])\s+decided|27\s+genuine,\s*(?:\d|[1-7]\d|80)\s+decided|28\s+genuine,\s*(?:\d|[1-7]\d|8[0-3])\s+decided|29\s+genuine,\s*(?:\d|[1-7]\d|8[0-6])\s+decided|30\s+genuine,\s*(?:\d|[1-8]\d)\s+decided)\b'
flags: i
---
