"""Site configuration: defaults.json, with an optional site.json over it."""

import json
from dataclasses import dataclass
from datetime import time
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULTS = PROJECT_ROOT / "defaults.json"
SITE_OVERRIDES = PROJECT_ROOT / "site.json"

DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


@dataclass(frozen=True)
class Receptor:
    id: str
    name: str


@dataclass(frozen=True)
class Config:
    site_timezone: str
    window_days: tuple  # weekday numbers, Monday is 0
    window_start: time
    window_end: time
    min_interval_minutes: int
    notice_hours: int
    ppv_limit_mm_s: float
    site_k: float
    site_b: float
    receptors: tuple
    outbox: str
    schedule_file: str

    @property
    def zone(self):
        return ZoneInfo(self.site_timezone)


def _clock(text):
    hours, minutes = text.split(":")
    return time(int(hours), int(minutes))


def from_dict(data):
    window = data["window"]
    constants = data["site_constants"]
    return Config(
        site_timezone=data["site_timezone"],
        window_days=tuple(DAY_NAMES.index(day) for day in window["days"]),
        window_start=_clock(window["start"]),
        window_end=_clock(window["end"]),
        min_interval_minutes=int(data["min_interval_minutes"]),
        notice_hours=int(data["notice_hours"]),
        ppv_limit_mm_s=float(data["ppv_limit_mm_s"]),
        site_k=float(constants["k"]),
        site_b=float(constants["b"]),
        receptors=tuple(Receptor(r["id"], r["name"]) for r in data["receptors"]),
        outbox=data["outbox"],
        schedule_file=data["schedule_file"],
    )


def load(path=DEFAULTS, override=SITE_OVERRIDES):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if override is not None and Path(override).exists():
        data.update(json.loads(Path(override).read_text(encoding="utf-8")))
    return from_dict(data)
