# Gaugefeed

Gaugefeed fetches the latest reading from each river gauge on the station list
and prints one JSON document for the dashboard. It runs once per cycle, started
from cron:

    python -m gaugefeed stations.txt

Stations that do not answer are left out of that cycle's document. The words
used here are defined in [docs/lexicon.md](docs/lexicon.md), and the decisions
behind the layout are in [docs/adr/](docs/adr/README.md).

## Development

    python3 -m unittest discover -s tests
