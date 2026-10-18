import unittest

from blastplan import window
from tests.support import make_config, utc


class WindowTest(unittest.TestCase):
    def setUp(self):
        self.cfg = make_config()

    def test_inside_window(self):
        self.assertTrue(window.is_permitted(utc(2030, 6, 18, 11), self.cfg))

    def test_both_ends_are_permitted(self):
        self.assertTrue(window.is_permitted(utc(2030, 6, 18, 10), self.cfg))
        self.assertTrue(window.is_permitted(utc(2030, 6, 18, 16), self.cfg))

    def test_after_end_minute(self):
        self.assertFalse(window.is_permitted(utc(2030, 6, 18, 16, 1), self.cfg))

    def test_weekend(self):
        self.assertFalse(window.is_permitted(utc(2030, 6, 22, 11), self.cfg))

    def test_local_time_in_summer(self):
        cfg = make_config(site_timezone="Europe/London")
        # 09:30 UTC is 10:30 BST
        self.assertTrue(window.is_permitted(utc(2030, 6, 18, 9, 30), cfg))
        # 15:30 UTC is 16:30 BST
        self.assertFalse(window.is_permitted(utc(2030, 6, 18, 15, 30), cfg))


if __name__ == "__main__":
    unittest.main()
