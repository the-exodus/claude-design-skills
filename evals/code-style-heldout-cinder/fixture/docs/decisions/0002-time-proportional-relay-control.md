# 0002. Time-proportional relay control over a two-second window

Status: Accepted

The elements are either on or off. Each control window lasts two seconds; the
controller picks a duty for the window and keeps the relay on for that share of
it. Only `Relay` drives the relay's pin, so that every path that switches the
elements, including an abort, goes through one place.
