import unittest

from blastplan import vibration
from tests.support import make_config


class VibrationTest(unittest.TestCase):
    def setUp(self):
        self.cfg = make_config()

    def test_typical_blast_is_within_limit(self):
        self.assertTrue(vibration.within_limit(180, 420, self.cfg))

    def test_heavy_charge_close_in_exceeds_limit(self):
        self.assertFalse(vibration.within_limit(400, 300, self.cfg))

    def test_prediction_is_rounded_up(self):
        ppv = vibration.predict_ppv(180, 420, self.cfg)
        self.assertEqual(ppv, round(ppv, 1))
        exact = self.cfg.site_k * (420 / 180 ** 0.5) ** -self.cfg.site_b
        self.assertGreaterEqual(ppv, exact)


if __name__ == "__main__":
    unittest.main()
