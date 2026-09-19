# Configuration

| Key | Default | Meaning |
|---|---|---|
| `poll_interval` | `5m` | How often each gauge is asked for a reading. |
| `max_reading_age` | `24h` | Readings older than this are rejected on arrival. |
| `data_dir` | `/var/lib/tidewatch` | Where the station databases live. |
