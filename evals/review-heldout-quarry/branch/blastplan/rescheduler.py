"""Moving blasts that have already been planned."""


class Rescheduler:
    """Postpones blasts on behalf of the command line."""

    def __init__(self, schedule):
        self._schedule = schedule

    @property
    def limit(self):
        return self._schedule.cfg.max_postponements

    def postpone(self, blast_id, new_time, now):
        return self._schedule.postpone(blast_id, new_time, now)
