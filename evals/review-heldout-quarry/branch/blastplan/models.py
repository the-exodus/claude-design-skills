"""The blast record."""

from dataclasses import dataclass
from datetime import datetime

PLANNED = "planned"
CANCELLED = "cancelled"
FIRED = "fired"


@dataclass
class Blast:
    id: str
    bench: str
    scheduled_at: datetime  # aware, UTC (ADR 0001)
    charge_kg: float  # maximum instantaneous charge
    distance_m: float  # to the nearest receptor
    status: str = PLANNED
    postponements: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "bench": self.bench,
            "scheduled_at": self.scheduled_at.isoformat(),
            "charge_kg": self.charge_kg,
            "distance_m": self.distance_m,
            "status": self.status,
            "postponements": self.postponements,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            bench=data["bench"],
            scheduled_at=datetime.fromisoformat(data["scheduled_at"]),
            charge_kg=float(data["charge_kg"]),
            distance_m=float(data["distance_m"]),
            status=data["status"],
            postponements=int(data.get("postponements", 0)),
        )
