# 0004. Schedules are checked once, at load

Status: Accepted

`Schedule::new` is the only way to build a schedule, and it rejects anything the
controller cannot follow: an empty schedule, more than eight segments, a zero
rate, a rate whose sign disagrees with its target, a heating segment after a
cooling one, and a target above the kiln limit. The controller trusts a
`Schedule` and does not check it again.
