# Assumptions

What Ferrybook's design relies on about Python and the host. Each says how we would know it stopped holding.

## A1: `json.load` keeps a file's key order

`config.load` and the timetable reader rely on dictionaries keeping the order of the file. **How we would know:** a settings dump or a timetable listing comes out in a different order from the file.

## A2: `time.monotonic()` counts from boot, so its values stay valid across restarts of the service

A deadline taken from `time.monotonic()` can be stored and compared after the service restarts on the same host. **How we would know:** a stored deadline is reached early or late after a restart.

## A3: `datetime.fromisoformat` accepts a trailing `Z`

The timetable export writes UTC times as `2026-06-01T07:30:00Z`, and `timetable.load` passes them to `datetime.fromisoformat` unchanged. True since Python 3.11. **How we would know:** loading the timetable raises `ValueError` on the first row.
