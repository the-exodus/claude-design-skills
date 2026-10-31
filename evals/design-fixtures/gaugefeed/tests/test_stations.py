import os
import tempfile
import unittest

from gaugefeed.stations import parse_station_list, read_station_list


class ParseStationListTest(unittest.TestCase):
    def test_one_url_per_line_in_order(self):
        text = "http://gauge-02.example/reading\nhttp://gauge-01.example/reading\n"
        self.assertEqual(
            parse_station_list(text),
            ["http://gauge-02.example/reading", "http://gauge-01.example/reading"],
        )

    def test_blank_lines_and_comments_are_skipped(self):
        text = "# upper river\nhttp://gauge-01.example/reading\n\n   \n# lower\n"
        self.assertEqual(parse_station_list(text), ["http://gauge-01.example/reading"])

    def test_surrounding_whitespace_is_stripped(self):
        self.assertEqual(
            parse_station_list("  http://gauge-01.example/reading  \n"),
            ["http://gauge-01.example/reading"],
        )

    def test_empty_list(self):
        self.assertEqual(parse_station_list(""), [])


class ReadStationListTest(unittest.TestCase):
    def test_reads_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "stations.txt")
            with open(path, "w", encoding="utf-8") as station_list:
                station_list.write("# test\nhttp://gauge-07.example/reading\n")
            self.assertEqual(read_station_list(path), ["http://gauge-07.example/reading"])


if __name__ == "__main__":
    unittest.main()
