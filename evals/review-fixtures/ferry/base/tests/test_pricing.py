import unittest

from ferrybook import pricing
from ferrybook.booking import BookingBook
from tests.helpers import sailing

SETTINGS = {"surge_threshold": 5, "surge_percent": 20}


class PricingTests(unittest.TestCase):
    def test_car_fare_without_surge(self):
        book = BookingBook([sailing(car_spaces=20)])
        self.assertEqual(pricing.car_fare("ARD-SKO", book, "S1", SETTINGS), 42000)

    def test_surge_when_few_car_spaces_are_left(self):
        book = BookingBook([sailing(car_spaces=4)])
        self.assertEqual(pricing.car_fare("ARD-SKO", book, "S1", SETTINGS), 50400)

    def test_child_fare_is_half_the_foot_fare(self):
        self.assertEqual(pricing.child_fare("SKO-HUS"), 3500)


if __name__ == "__main__":
    unittest.main()
