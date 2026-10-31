"""Runs one cycle: fetches every station on the list and prints the report."""

import sys
from datetime import datetime, timezone

from gaugefeed import fetcher, report, stations


def main(argv: list[str]) -> int:
    """Run a cycle over the station list named in argv; return the exit status."""
    if len(argv) != 2:
        print("usage: python -m gaugefeed STATION_LIST", file=sys.stderr)
        return 2
    station_urls = stations.read_station_list(argv[1])
    readings = fetcher.fetch_all(station_urls)
    print(report.build_report(readings, datetime.now(timezone.utc)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
