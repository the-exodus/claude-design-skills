# Artisan on the roaster laptop

The roaster runs Artisan on the same laptop as Roastlog, and Artisan writes
its own records into `roastlog.db` (ADR-0001).

From the moment a roast is charged until it is dropped, Artisan holds a write
lock on `roastlog.db`. Any other writer in that window waits for the lock and
gives up after SQLite's busy timeout with `database is locked`. Readers are not
affected: the file is in WAL mode.

Between roasts Artisan holds no lock.
