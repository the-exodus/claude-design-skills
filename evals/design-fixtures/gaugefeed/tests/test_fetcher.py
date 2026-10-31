import io
import unittest
import urllib.error
from unittest import mock

from gaugefeed import fetcher


class FetchReadingTest(unittest.TestCase):
    @mock.patch("urllib.request.urlopen")
    def test_returns_the_decoded_reading(self, urlopen):
        urlopen.return_value = io.BytesIO(b'{"level_m": 1.42}')
        self.assertEqual(
            fetcher.fetch_reading("http://gauge-01.example/reading"), {"level_m": 1.42}
        )
        urlopen.assert_called_once_with("http://gauge-01.example/reading", timeout=5.0)

    @mock.patch("urllib.request.urlopen")
    def test_station_that_does_not_answer_raises(self, urlopen):
        urlopen.side_effect = urllib.error.URLError("timed out")
        with self.assertRaises(urllib.error.URLError):
            fetcher.fetch_reading("http://gauge-01.example/reading")


class FetchAllTest(unittest.TestCase):
    def test_fetches_every_station(self):
        levels = {"http://a.example": {"level_m": 1.0}, "http://b.example": {"level_m": 2.0}}
        with mock.patch.object(fetcher, "fetch_reading", side_effect=levels.get):
            self.assertEqual(fetcher.fetch_all(list(levels)), levels)

    def test_skips_stations_that_do_not_answer(self):
        def fetch(url):
            if url == "http://down.example":
                raise urllib.error.URLError("connection refused")
            return {"level_m": 1.0}

        with mock.patch.object(fetcher, "fetch_reading", side_effect=fetch):
            readings = fetcher.fetch_all(["http://down.example", "http://up.example"])
        self.assertEqual(readings, {"http://up.example": {"level_m": 1.0}})

    def test_timeout_counts_as_not_answering(self):
        with mock.patch.object(fetcher, "fetch_reading", side_effect=TimeoutError):
            self.assertEqual(fetcher.fetch_all(["http://slow.example"]), {})


if __name__ == "__main__":
    unittest.main()
