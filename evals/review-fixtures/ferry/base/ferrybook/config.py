import json
from pathlib import Path

DEFAULTS = Path(__file__).resolve().parent.parent / "defaults.json"


def load(path=DEFAULTS):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
