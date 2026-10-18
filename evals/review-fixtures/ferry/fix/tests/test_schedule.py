import unittest
from datetime import datetime, timezone

from ferrybook.schedule import departures_on
from tests.helpers import sailing

JUNE_1 = datetime(2026, 6, 1, tzinfo=timezone.utc)


class ScheduleTests(unittest.TestCase):
    def test_departures_on_a_day(self):
        morning = sailing(id="S1", departs="2026-06-01T07:30:00")
        next_day = sailing(id="S2", departs="2026-06-02T07:30:00")
        self.assertEqual([s.id for s in departures_on([morning, next_day], JUNE_1)], ["S1"])

    def test_a_midnight_sailing_is_not_listed_on_the_day_before(self):
        midnight = sailing(id="S3", departs="2026-06-02T00:00:00", arrives="2026-06-02T00:40:00")
        self.assertEqual(departures_on([midnight], JUNE_1), [])


if __name__ == "__main__":
    unittest.main()
