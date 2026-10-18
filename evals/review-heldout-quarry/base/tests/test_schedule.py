import unittest

from blastplan.models import CANCELLED
from blastplan.schedule import Schedule, ScheduleError
from tests.support import blast, make_config, utc


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule(make_config())

    def test_add_keeps_firing_order(self):
        self.schedule.add(blast("B2", utc(2030, 6, 18, 14)))
        self.schedule.add(blast("B1", utc(2030, 6, 18, 10)))
        self.assertEqual([b.id for b in self.schedule], ["B1", "B2"])

    def test_outside_window_refused(self):
        with self.assertRaises(ScheduleError):
            self.schedule.add(blast("B1", utc(2030, 6, 18, 17)))

    def test_too_close_refused(self):
        self.schedule.add(blast("B1", utc(2030, 6, 18, 11)))
        with self.assertRaises(ScheduleError):
            self.schedule.add(blast("B2", utc(2030, 6, 18, 12)))

    def test_exactly_min_interval_allowed(self):
        self.schedule.add(blast("B1", utc(2030, 6, 18, 11)))
        self.schedule.add(blast("B2", utc(2030, 6, 18, 12, 30)))

    def test_vibration_limit_refused(self):
        with self.assertRaises(ScheduleError):
            self.schedule.add(blast("B1", utc(2030, 6, 18, 11), charge=400, distance=300))

    def test_cancelled_blast_stays_and_frees_its_slot(self):
        self.schedule.add(blast("B1", utc(2030, 6, 18, 11)))
        self.schedule.cancel("B1")
        self.assertEqual(self.schedule.get("B1").status, CANCELLED)
        self.schedule.add(blast("B2", utc(2030, 6, 18, 11, 30)))

    def test_id_never_reused(self):
        self.schedule.add(blast("B1", utc(2030, 6, 18, 11)))
        self.schedule.cancel("B1")
        with self.assertRaises(ScheduleError):
            self.schedule.add(blast("B1", utc(2030, 6, 19, 11)))

    def test_next_blast(self):
        self.schedule.add(blast("B1", utc(2030, 6, 18, 11)))
        self.schedule.add(blast("B2", utc(2030, 6, 18, 14)))
        self.assertEqual(self.schedule.next_blast(utc(2030, 6, 18, 12)).id, "B2")


if __name__ == "__main__":
    unittest.main()
