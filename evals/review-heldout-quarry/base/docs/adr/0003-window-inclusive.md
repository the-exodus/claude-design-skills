# 0003. The permitted window is inclusive at both ends

Status: Accepted

## Context

Condition 14 of the planning permission says blasting may take place
"between 10:00 and 16:00 inclusive, Monday to Friday". The shotfirer often
plans the last blast of the day for exactly 16:00.

## Decision

A blast at exactly the window's start or end time is permitted. Every check
or search against the window treats `end` as the last permitted firing time,
not as the first forbidden one.

Rejected: a half-open window `[start, end)`, which is the usual programming
convention but would refuse a 16:00 blast the permission allows.

## Consequences

Comparisons against `window.end` use `<=`. A time with seconds past the end
minute (16:00:30) is outside the window.
