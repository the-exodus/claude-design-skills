import json
import os
import tempfile
import unittest

from gaugefeed.archive import pack_month


def save(directory, name, document):
    with open(os.path.join(directory, name), "w", encoding="utf-8") as saved:
        json.dump(document, saved)


class PackMonthTest(unittest.TestCase):
    def test_packs_the_month_in_cycle_order(self):
        with tempfile.TemporaryDirectory() as directory:
            save(directory, "2025-06-01T12:10:00+00:00.json", {"cycle": "12:10"})
            save(directory, "2025-06-01T12:05:00+00:00.json", {"cycle": "12:05"})
            save(directory, "2025-07-01T00:00:00+00:00.json", {"cycle": "july"})
            archive = json.loads(pack_month(directory, "2025-06"))
        self.assertEqual(archive["month"], "2025-06")
        self.assertEqual(archive["cycles"], [{"cycle": "12:05"}, {"cycle": "12:10"}])

    def test_a_month_with_nothing_saved_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(json.loads(pack_month(directory, "2025-06"))["cycles"], [])


if __name__ == "__main__":
    unittest.main()
