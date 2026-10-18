"""Keeps the schedule in a JSON file, in firing order."""

import json
import os
from pathlib import Path

from .models import Blast
from .schedule import Schedule


def load(path, cfg):
    path = Path(path)
    if not path.exists():
        return Schedule(cfg)
    data = json.loads(path.read_text(encoding="utf-8"))
    return Schedule(cfg, [Blast.from_dict(d) for d in data["blasts"]])


def save(schedule, path):
    path = Path(path)
    data = {"blasts": [blast.to_dict() for blast in schedule]}
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
