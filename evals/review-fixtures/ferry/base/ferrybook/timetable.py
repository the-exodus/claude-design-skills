"""Reads the operator's timetable export."""
import json
from datetime import datetime

from .schedule import Sailing


def load(path):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    # The export writes UTC times with a trailing Z (assumptions.md, A3).
    return [
        Sailing(
            id=row["id"],
            route=row["route"],
            departs=datetime.fromisoformat(row["departs"]),
            arrives=datetime.fromisoformat(row["arrives"]),
            car_spaces=row["car_spaces"],
            foot_spaces=row["foot_spaces"],
        )
        for row in rows
    ]
