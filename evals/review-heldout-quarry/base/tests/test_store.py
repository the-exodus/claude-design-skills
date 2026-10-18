import tempfile
import unittest
from pathlib import Path

from blastplan import store
from blastplan.schedule import Schedule
from tests.support import blast, make_config, utc


class StoreTest(unittest.TestCase):
    def test_round_trip_keeps_order_and_status(self):
        cfg = make_config()
        schedule = Schedule(cfg)
        schedule.add(blast("B2", utc(2030, 6, 18, 14)))
        schedule.add(blast("B1", utc(2030, 6, 18, 10)))
        schedule.cancel("B2")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "schedule.json"
            store.save(schedule, path)
            loaded = store.load(path, cfg)
        self.assertEqual([(b.id, b.status) for b in loaded],
                         [("B1", "planned"), ("B2", "cancelled")])
        self.assertEqual(loaded.get("B1").scheduled_at, utc(2030, 6, 18, 10))


if __name__ == "__main__":
    unittest.main()
