# Assumptions

Things outside this code that the design relies on, and how we would notice
one had stopped holding.

## A1. A time zone database is available

`zoneinfo.ZoneInfo(site_timezone)` finds the IANA database: the system one on
Linux, and on the site office PC the `tzdata` package installed by the office
image (the one thing outside the standard library).
*Stops holding:* `ZoneInfoNotFoundError` when the configuration is loaded.

## A2. astimezone applies daylight saving correctly

Converting an aware UTC datetime with `astimezone(ZoneInfo("Europe/London"))`
gives the local wall-clock time with the offset in force at that instant,
including on the days the clocks change.
*Stops holding:* the window tests around the last Sundays of March and
October fail.

## A3. Renaming a file into place replaces it atomically

Notices are written to a temporary file and renamed into place with
`os.rename`, so the office never picks up a half-written notice. A rename
onto an existing name replaces that file atomically on Linux and on Windows
alike, so the same helper serves if a notice file is ever rewritten.
*Stops holding:* the office finds truncated notice files, or the helper
raises when the destination exists.

## A4. The site PC clock is synchronised

`cli.py` takes `now` from the system clock, and notice lead times are
computed from it. The office PC syncs with an NTP server, so it is within a
minute of true time.
*Stops holding:* the "Issued" time on notices disagrees with the office's
sent-mail timestamps by more than a minute.
