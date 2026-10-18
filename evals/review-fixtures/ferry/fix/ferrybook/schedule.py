from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Sailing:
    id: str
    route: str
    departs: datetime
    arrives: datetime
    car_spaces: int
    foot_spaces: int


def departures_on(sailings, day_start):
    """Sailings departing on the day that starts at day_start."""
    day_end = day_start + timedelta(days=1)
    return [s for s in sailings if day_start < s.departs < day_end]


def arrivals_on(sailings, day_start):
    """Sailings arriving on the day that starts at day_start."""
    day_end = day_start + timedelta(days=1)
    return [s for s in sailings if day_start <= s.arrives <= day_end]
