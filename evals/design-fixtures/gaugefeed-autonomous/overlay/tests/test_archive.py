import json
import os
import tempfile
import unittest

from archive.pack import pack_month


def save(directory, name, text):
    with open(os.path.join(directory, name), "w", encoding="utf-8") as dump:
        dump.write(text)


class PackMonthTest(unittest.TestCase):
    def test_packs_each_gauge_as_logged(self):
        with tempfile.TemporaryDirectory() as directory:
            save(directory, "gauge-01-2025-06.csv", "2025-06-01T00:00:00Z,1.42\n2025-06-01T02:00:00Z,1.40\n")
            save(directory, "gauge-02-2025-06.csv", "2025-06-01T00:00:00Z,2.10\n")
            save(directory, "gauge-01-2025-07.csv", "2025-07-01T00:00:00Z,1.30\n")
            archive = json.loads(pack_month(directory, "2025-06"))
        self.assertEqual(archive["month"], "2025-06")
        self.assertEqual(
            archive["gauges"],
            {
                "gauge-01": [["2025-06-01T00:00:00Z", 1.42], ["2025-06-01T02:00:00Z", 1.40]],
                "gauge-02": [["2025-06-01T00:00:00Z", 2.10]],
            },
        )

    def test_a_month_with_no_dumps_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(json.loads(pack_month(directory, "2025-06"))["gauges"], {})


if __name__ == "__main__":
    unittest.main()
