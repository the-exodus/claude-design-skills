# Gaugefeed

Gaugefeed fetches the latest reading from each river gauge on the station list
and prints one JSON document for the dashboard. It runs once per cycle, started
from cron:

    python -m gaugefeed stations.txt

Stations that do not answer are left out of that cycle's document. The words
used here are defined in [docs/lexicon.md](docs/lexicon.md), and the decisions
behind the layout are in [docs/adr/](docs/adr/README.md).

Each gauge also logs its level every hour. Field staff save the logger dumps
under `dumps/`, and once a month the records office's archive is packed from
them:

    python -m gaugefeed.archive dumps/ 2025-06

## Development

    python3 -m unittest discover -s tests
