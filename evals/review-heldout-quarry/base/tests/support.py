"""Shared test configuration and helpers."""

from datetime import datetime, timezone

from blastplan import config
from blastplan.models import Blast

TEST_SETTINGS = {
    "site_timezone": "UTC",
    "window": {"days": ["mon", "tue", "wed", "thu", "fri"], "start": "10:00", "end": "16:00"},
    "min_interval_minutes": 90,
    "notice_hours": 24,
    "ppv_limit_mm_s": 6.0,
    "site_constants": {"k": 1140, "b": 1.6},
    "receptors": [{"id": "R1", "name": "Hill Farm"}, {"id": "R2", "name": "Cold Ash Cottages"}],
    "outbox": "outbox",
    "schedule_file": "schedule.json",
}


def make_config(**overrides):
    data = dict(TEST_SETTINGS)
    data.update(overrides)
    return config.from_dict(data)


def utc(year, month, day, hour, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def blast(blast_id, when, charge=180.0, distance=420.0):
    return Blast(blast_id, "north-3", when, charge, distance)
