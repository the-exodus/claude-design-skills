import json
import unittest
from datetime import datetime, timezone

from gaugefeed.report import build_report

CYCLE = datetime(2025, 6, 1, 12, 5, tzinfo=timezone.utc)


class BuildReportTest(unittest.TestCase):
    def test_carries_the_cycle_time(self):
        document = json.loads(build_report({}, CYCLE))
        self.assertEqual(document["cycle"], "2025-06-01T12:05:00+00:00")

    def test_one_entry_per_reading_sorted_by_station(self):
        readings = {
            "http://gauge-02.example/reading": {"level_m": 2.10},
            "http://gauge-01.example/reading": {"level_m": 1.42},
        }
        document = json.loads(build_report(readings, CYCLE))
        self.assertEqual(
            document["stations"],
            [
                {"station": "http://gauge-01.example/reading", "reading": {"level_m": 1.42}},
                {"station": "http://gauge-02.example/reading", "reading": {"level_m": 2.10}},
            ],
        )

    def test_no_readings_gives_an_empty_station_list(self):
        document = json.loads(build_report({}, CYCLE))
        self.assertEqual(document["stations"], [])


if __name__ == "__main__":
    unittest.main()
