# 0001. Times are UTC inside the program

Status: Accepted

## Context

The permitted window and the notices are in UK local time, which changes
offset twice a year. Local wall-clock times are ambiguous in the autumn hour
and missing in the spring hour, and comparing them across a change gives wrong
intervals.

## Decision

Every datetime held by the program is an aware datetime in UTC. Site local
time is used only at the edges: parsing command-line input, checking the
permitted window (`window.py`), and writing notice text. Intervals (spacing,
notice lead) are computed between UTC datetimes.

Rejected: storing site-local times with their zone, because interval
arithmetic between two datetimes sharing a `ZoneInfo` is wall-clock
arithmetic in Python and is wrong across a change.

## Consequences

Anything that builds a time from a local date and a local clock time must
attach `site_timezone` and convert to UTC before using it.
