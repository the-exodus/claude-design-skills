import tempfile
import unittest
from pathlib import Path

from blastplan import notices
from blastplan.schedule import PostponeLimitError, Schedule, ScheduleError
from tests.support import blast, make_config, utc

NOW = utc(2030, 6, 14, 9)  # Friday


class PostponeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = make_config(outbox=self.tmp.name)
        self.schedule = Schedule(self.cfg)
        self.schedule.add(blast("B1", utc(2030, 6, 17, 10)))

    def test_postpone_keeps_id_and_moves(self):
        moved = self.schedule.postpone("B1", utc(2030, 6, 17, 14), NOW)
        self.assertEqual(moved.id, "B1")
        self.assertEqual(self.schedule.get("B1").scheduled_at, utc(2030, 6, 17, 14))
        self.assertEqual(moved.postponements, 1)

    def test_earlier_time_refused(self):
        with self.assertRaises(ScheduleError):
            self.schedule.postpone("B1", utc(2030, 6, 17, 9), NOW)

    def test_outside_window_refused(self):
        with self.assertRaises(ScheduleError):
            self.schedule.postpone("B1", utc(2030, 6, 17, 17), NOW)

    def test_clash_refused(self):
        self.schedule.add(blast("B2", utc(2030, 6, 17, 13)))
        with self.assertRaises(ScheduleError):
            self.schedule.postpone("B1", utc(2030, 6, 17, 12), NOW)

    def test_short_notice_refused(self):
        with self.assertRaises(ScheduleError):
            self.schedule.postpone("B1", utc(2030, 6, 17, 14), utc(2030, 6, 17, 9))

    def test_next_free_slot_skips_other_blasts(self):
        self.schedule.add(blast("B2", utc(2030, 6, 18, 10)))
        moved = self.schedule.postpone("B1", None, utc(2030, 6, 17, 9))
        self.assertEqual(moved.scheduled_at, utc(2030, 6, 18, 11, 30))

    def test_next_free_slot_rolls_over_weekend(self):
        moved = self.schedule.postpone("B1", None, utc(2030, 6, 20, 17))
        self.assertEqual(moved.scheduled_at, utc(2030, 6, 24, 10))

    def test_limit(self):
        cfg = make_config(outbox=self.tmp.name, max_postponements=1)
        schedule = Schedule(cfg, [blast("B1", utc(2030, 6, 17, 10))])
        schedule.postpone("B1", utc(2030, 6, 17, 12), NOW)
        with self.assertRaises(PostponeLimitError):
            schedule.postpone("B1", utc(2030, 6, 17, 14), NOW)

    def test_cancelled_blast_cannot_be_postponed(self):
        self.schedule.cancel("B1")
        with self.assertRaises(ScheduleError):
            self.schedule.postpone("B1", utc(2030, 6, 17, 14), NOW)

    def test_revised_notice_replaces_original(self):
        notices.issue_notices(self.schedule.get("B1"), self.cfg, NOW)
        self.schedule.postpone("B1", utc(2030, 6, 18, 11), NOW)
        files = sorted(Path(self.tmp.name).glob("notice-B1-*.txt"))
        self.assertEqual([f.name for f in files], ["notice-B1-R1.txt", "notice-B1-R2.txt"])
        text = files[0].read_text(encoding="utf-8")
        self.assertIn("REVISED NOTICE", text)
        self.assertIn("Tuesday 18 June 2030 at 11:00", text)

    def test_no_revised_notice_before_notify(self):
        self.schedule.postpone("B1", utc(2030, 6, 18, 11), NOW)
        self.assertEqual(list(Path(self.tmp.name).glob("*.txt")), [])


if __name__ == "__main__":
    unittest.main()
