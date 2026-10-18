# 0004. The clock is passed in

Status: Accepted

## Context

Notice lead times, the "next blast" and similar rules depend on the current
time. Code that reads the clock itself cannot be tested at a chosen moment
and records times the caller did not decide.

## Decision

Only `cli.py` reads the clock (`datetime.now(timezone.utc)`). Every other
function that needs the current time takes it as a `now` argument.

Rejected: calling `datetime.now()` where it is needed, which hides the
dependency and makes two checks in one operation see two different times.

## Consequences

Functions grow a `now` parameter. Tests pass fixed times.
