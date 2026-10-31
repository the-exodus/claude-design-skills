# Gaugefeed

Gaugefeed fetches the latest reading from each river gauge on the station list
and prints one JSON document for the dashboard. It runs once per cycle, started
from cron:

    python -m gaugefeed stations.txt

Stations that do not answer are left out of that cycle's document. The words
used here are defined in [docs/lexicon.md](docs/lexicon.md), and the decisions
behind the layout are in [docs/adr/](docs/adr/README.md).

Cron saves each cycle's document under `documents/`, and once a month the
records office's archive is packed from them:

    python -m gaugefeed.archive documents/ 2025-06

## Development

    python3 -m unittest discover -s tests
