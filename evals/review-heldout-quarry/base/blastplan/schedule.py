"""The blast schedule: planned, cancelled and fired blasts in firing order."""

import bisect
from datetime import timedelta

from . import vibration, window
from .models import CANCELLED, PLANNED


class ScheduleError(Exception):
    pass


def _firing_order(blast):
    return blast.scheduled_at


class Schedule:
    def __init__(self, cfg, blasts=()):
        """`blasts` must already be in firing order; the store saves them so."""
        self.cfg = cfg
        self._blasts = list(blasts)

    def __iter__(self):
        return iter(self._blasts)

    def get(self, blast_id):
        for blast in self._blasts:
            if blast.id == blast_id:
                return blast
        raise ScheduleError(f"no blast {blast_id}")

    def add(self, blast):
        if any(b.id == blast.id for b in self._blasts):
            raise ScheduleError(f"blast id {blast.id} has already been used")
        self._check_rules(blast.scheduled_at, blast.id)
        if not vibration.within_limit(blast.charge_kg, blast.distance_m, self.cfg):
            ppv = vibration.predict_ppv(blast.charge_kg, blast.distance_m, self.cfg)
            raise ScheduleError(
                f"predicted PPV {ppv} mm/s exceeds the {self.cfg.ppv_limit_mm_s} mm/s limit"
            )
        bisect.insort(self._blasts, blast, key=_firing_order)
        return blast

    def cancel(self, blast_id):
        blast = self.get(blast_id)
        if blast.status != PLANNED:
            raise ScheduleError(f"blast {blast_id} is {blast.status}")
        blast.status = CANCELLED  # it stays in the schedule (ADR 0002)
        return blast

    def next_blast(self, now):
        """The first planned blast at or after `now`, or None."""
        for blast in self._blasts:
            if blast.status == PLANNED and blast.scheduled_at >= now:
                return blast
        return None

    def _check_rules(self, when, blast_id):
        if not window.is_permitted(when, self.cfg):
            raise ScheduleError(f"{when:%Y-%m-%d %H:%M} UTC is outside the permitted window")
        clash = self._clash(when, blast_id)
        if clash is not None:
            raise ScheduleError(
                f"less than {self.cfg.min_interval_minutes} minutes from blast {clash.id}"
            )

    def _clash(self, when, ignore_id=None):
        """A planned blast closer to `when` than the minimum interval, or None.

        Only the planned neighbours either side of `when` are looked at, which
        is enough because the schedule is kept in firing order.
        """
        planned = [b for b in self._blasts if b.status == PLANNED and b.id != ignore_id]
        times = [b.scheduled_at for b in planned]
        i = bisect.bisect_left(times, when)
        gap = timedelta(minutes=self.cfg.min_interval_minutes)
        for j in (i - 1, i):
            if 0 <= j < len(planned) and abs(planned[j].scheduled_at - when) < gap:
                return planned[j]
        return None
