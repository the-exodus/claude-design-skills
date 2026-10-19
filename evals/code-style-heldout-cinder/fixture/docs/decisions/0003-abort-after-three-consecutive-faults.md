# 0003. Abort after three consecutive sensor faults

Status: Accepted

Single open-circuit frames show up on the studio kiln when the elements switch.
Aborting on the first one ended good firings, so a firing now aborts on the
third consecutive faulty frame (six seconds of them). A good frame in between
resets the count. Until then the controller carries on with the last good
temperature.
