# blastplan

A small planning tool for the shotfirer and site office at Cold Ash quarry.
It keeps the blast schedule, refuses blasts the planning permission does not
allow, and writes the notices that neighbours must receive before each blast.

Runs on Linux and on the site office PC (Windows).

## Usage

    python3 -m blastplan.cli add B14 north-3 "2030-06-18 11:00" --charge 180 --distance 420
    python3 -m blastplan.cli notify B14
    python3 -m blastplan.cli list
    python3 -m blastplan.cli status
    python3 -m blastplan.cli postpone B14 --to "2030-06-19 10:30"
    python3 -m blastplan.cli cancel B14

Times on the command line are site local time (`YYYY-MM-DD HH:MM`).

- `add` plans a blast. It is refused if the time is outside the permitted
  window, if it is closer than `min_interval_minutes` to another planned blast,
  or if the predicted peak particle velocity at the nearest receptor exceeds
  `ppv_limit_mm_s`. Blast ids are never reused, not even after a cancellation.
- `notify` writes one notice per receptor into the outbox. It is refused if the
  blast is less than `notice_hours` away.
- `list` shows every blast in firing order, with its status.
- `status` shows, for each planned blast, the hours of notice a neighbour would
  get if notified now, and marks it `SHORT NOTICE` when that is under
  `notice_hours`.
- `postpone` moves a planned blast to a later time, keeping its id. Without
  `--to` it picks the earliest free slot at least `notice_hours` from now. The
  new time must pass the same window and spacing rules as `add`. Receptors
  already notified get a revised notice. A blast can be postponed at most
  `max_postponements` times; after that, cancel it and plan a new blast.
- `cancel` marks a blast cancelled. Cancelled blasts stay in the schedule.

## Notices

Each notice is a plain-text file `outbox/notice-<blast>-<receptor>.txt`. The
site office prints or emails them; blastplan never contacts anyone itself.
Notice files are never modified after they are written, so the outbox doubles
as the record of what each neighbour was told.

## Configuration

Settings are read from `defaults.json`. A `site.json` next to it, if present,
overrides any top-level key.

| Key | Default | Meaning |
| --- | --- | --- |
| `site_timezone` | `Europe/London` | Zone the permitted window and notices are expressed in |
| `window.days` | `mon`–`fri` | Days on which blasting is permitted |
| `window.start` / `window.end` | `10:00` / `16:00` | Permitted firing times, both inclusive |
| `min_interval_minutes` | `90` | Minimum time between two planned blasts |
| `notice_hours` | `24` | Minimum notice a receptor must get before a blast |
| `max_postponements` | `2` | How many times one blast may be postponed |
| `ppv_limit_mm_s` | `6.0` | Planning limit on predicted peak particle velocity |
| `site_constants.k` / `.b` | `1140` / `1.6` | Site law constants for the vibration prediction |
| `receptors` | three neighbours | Who receives notices |
| `outbox` | `outbox` | Directory notices are written to |
| `schedule_file` | `schedule.json` | Where the schedule is kept |
