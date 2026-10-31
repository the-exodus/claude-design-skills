"""Reads the station list."""


def parse_station_list(text: str) -> list[str]:
    """Return the station URLs in the list, in order.

    One URL per line; blank lines and lines starting with # are skipped.
    """
    urls = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def read_station_list(path: str) -> list[str]:
    """Return the station URLs in the list file at path."""
    with open(path, encoding="utf-8") as station_list:
        return parse_station_list(station_list.read())
