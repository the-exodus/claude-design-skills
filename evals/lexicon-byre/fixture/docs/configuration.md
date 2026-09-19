# Configuration, lists and reports

Byre reads one file, `byre.yaml`, at start-up. Change it and restart. A
setting you leave out takes its default.

## Settings

| Key | Default | What it means |
| --- | --- | --- |
| `herd_name` | (none) | Printed at the top of every list and report. |
| `sessions_per_day` | 2 | How many sessions the farm milks each day, 2 or 3. |
| `session_close_minutes` | 45 | A session closes this long after its last milking. Readings that arrive later still count towards it; see [decision 0002](decisions/0002-late-readings-belong-to-their-session.md). |
| `gestation_days` | 283 | Days from the last service to the expected calving date. |
| `dry_period_days` | 60 | The target dry period. The due dry-off date is this many days before the expected calving date. |
| `dry_off_notice_days` | 7 | A cow goes on the dry-off list this many days before her due dry-off date. |
| `vwp_days` | 50 | The voluntary waiting period (VWP). A cow is not put on the serve list until she is this many days in milk. |
| `close_up_days` | 21 | Byre suggests moving a dry cow or an in-calf heifer to the close-up group this many days before she is due to calve. |
| `groups` | milkers, dry, close-up, heifers | The farm's management groups, in the order they print. |

## The daily lists

Every list shows the ear tag, name, management group, parity and, for a cow
in lactation, days in milk (DIM). A list is built afresh from the records
each time someone asks for it, so it is never out of date.

**Withhold list.** Every cow with an open milk withdrawal, with the product
and the date and time the withdrawal ends. The list is complete before the
session opens: a cow treated ten minutes before milking is on it. It is
rebuilt by the withhold sweep when a session opens. Milk from a cow on this
list is recorded but never counted as saleable.

**Dry-off list.** Cows within `dry_off_notice_days` of their due dry-off
date, soonest first. Heifers never appear, having no lactation to end. A cow
with no service on record has no expected calving date and so never appears
either; see [decision 0003](decisions/0003-dry-off-date-from-expected-calving.md).

**Calving list.** Every cow and in-calf heifer due to calve in the next 21
days, soonest first, with her expected calving date and the sire of the last
service.

**Serve list.** Cows past their VWP with no service since calving, and cows
whose last service was more than 24 days ago with no pregnancy confirmed.
Maiden heifers go on by age, at 13 months.

**Cull list.** Animals the herd manager has marked to leave the herd. An
animal with an open meat withdrawal is shown as not saleable, with the date
it ends. A milk withdrawal does not keep an animal off this list, and a meat
withdrawal does not put a cow on the withhold list; see
[decision 0001](decisions/0001-milk-and-meat-withdrawal-tracked-separately.md).

## Reports

**Daily yield.** Saleable and withheld kilograms per session and per day,
with the number of cows milked. A day's figures are final the following
morning, because late readings can still change a closed session.

**Medicine record.** Every treatment in a date range: animal, product, batch,
dose, last dose given, who gave it, and the end of the milk and the meat
withdrawal. This is the record an inspector asks for.

**Lactation summary.** Per cow: parity, calving date, days in milk, total
yield to date, services this lactation and expected calving date.
