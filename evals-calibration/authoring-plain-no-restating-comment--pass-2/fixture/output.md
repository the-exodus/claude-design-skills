from dataclasses import dataclass
from datetime import datetime


@dataclass
class Roast:
    batch_lot: str
    charged_at: datetime
    green_weight_g: float
    dropped_at: datetime | None = None
    first_crack_at: datetime | None = None
    roasted_weight_g: float | None = None


class RoastLog:
    def __init__(self) -> None:
        self._roasts: list[Roast] = []

    def add(self, roast: Roast) -> None:
        self._roasts.append(roast)

    def on(self, day: str) -> list[Roast]:
        return [r for r in self._roasts if r.charged_at.date().isoformat() == day]

    def count_on(self, day: str) -> int:
        return len(self.on(day))
