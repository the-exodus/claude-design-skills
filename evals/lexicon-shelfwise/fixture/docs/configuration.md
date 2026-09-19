# Configuration

Shelfwise reads `shelfwise.config.json` at startup. Any key you leave out
takes its default. This page is for library administrators.

## Loans

| Key | Default | Meaning |
|-----|---------|---------|
| `loans.loanPeriodDays` | 21 | Days from checkout (or renewal) to the due date. |
| `loans.gracePeriodDays` | 2 | Grace period: days after the due date before a loan is overdue and fines start. |
| `loans.maxRenewals` | 3 | How many times a patron may renew one loan. |
| `loans.maxExtensionDays` | 7 | Most days a single extension may add to a due date. |

## Fines

| Key | Default | Meaning |
|-----|---------|---------|
| `fines.dailyRateCents` | 25 | Fine per overdue day, in cents. |
| `fines.capCents` | 1000 | Most a single loan's fine can reach. |

## Holds

| Key | Default | Meaning |
|-----|---------|---------|
| `holds.pickupWindowDays` | 7 | Days a patron has to collect a held item once it is ready. |

## Maintenance

| Key | Default | Meaning |
|-----|---------|---------|
| `reconciler.sweepCron` | `0 3 * * *` | When the nightly charge sweep runs (cron syntax). Schedule it after the fine run. |
