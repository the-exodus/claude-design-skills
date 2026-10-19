"""Fetches a station's latest reading over HTTP."""

import json
import urllib.request


def fetch_reading(station_url: str, timeout: float = 5.0) -> dict:
    """Return the station's latest reading as a dict.

    Raises urllib.error.URLError when the station does not answer.
    """
    with urllib.request.urlopen(station_url, timeout=timeout) as response:
        return json.loads(response.read())


def fetch_all(station_urls: list[str]) -> dict[str, dict]:
    """Fetch every station, skipping the ones that do not answer."""
    readings = {}
    for url in station_urls:
        try:
            readings[url] = fetch_reading(url)
        except OSError:
            continue
    return readings
