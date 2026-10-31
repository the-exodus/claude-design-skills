"""Builds the dashboard's JSON document from a cycle's readings."""

import json
from datetime import datetime


def build_report(readings: dict[str, dict], cycle_time: datetime) -> str:
    """Return the cycle's document as JSON, one entry per station that answered.

    readings maps each station URL to its reading; stations appear sorted by URL.
    """
    document = {
        "cycle": cycle_time.isoformat(),
        "stations": [
            {"station": url, "reading": readings[url]} for url in sorted(readings)
        ],
    }
    return json.dumps(document, indent=2)
