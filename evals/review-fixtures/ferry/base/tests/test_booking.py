import unittest

from ferrybook.booking import BookingBook, FullError
from tests.helpers import sailing


class BookingTests(unittest.TestCase):
    def test_a_booking_takes_a_car_space(self):
        book = BookingBook([sailing(car_spaces=3)])
        book.book("S1", "Ada", vehicle=True)
        self.assertEqual(book.available_cars("S1"), 2)

    def test_reserved_spaces_are_never_sold(self):
        book = BookingBook([sailing(car_spaces=3)], reserved_car_spaces=2)
        book.book("S1", "Ada", vehicle=True)
        with self.assertRaises(FullError):
            book.book("S1", "Bo", vehicle=True)

    def test_cancelling_frees_the_space(self):
        book = BookingBook([sailing(car_spaces=1)])
        b = book.book("S1", "Ada", vehicle=True)
        book.cancel(b.ref)
        self.assertEqual(book.available_cars("S1"), 1)

    def test_references_go_up(self):
        book = BookingBook([sailing()])
        first = book.book("S1", "Ada")
        second = book.book("S1", "Bo")
        self.assertGreater(second.ref, first.ref)


if __name__ == "__main__":
    unittest.main()
