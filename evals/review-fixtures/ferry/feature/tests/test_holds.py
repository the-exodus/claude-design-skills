import os
import tempfile
import unittest

from ferrybook import pricing
from ferrybook.booking import BookingBook, FullError, HoldExpired
from ferrybook.holds import HoldDesk
from tests.helpers import sailing


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now

    def advance(self, minutes):
        self.now += minutes * 60


def make(car_spaces=2, **kwargs):
    clock = FakeClock()
    return BookingBook([sailing(car_spaces=car_spaces)], hold_minutes=15, clock=clock, **kwargs), clock


class HoldTests(unittest.TestCase):
    def test_a_hold_lasts_hold_minutes(self):
        book, clock = make()
        b = book.book("S1", "Ada", vehicle=True)
        clock.advance(14)
        self.assertEqual(book.get(b.ref).status, "held")
        clock.advance(2)
        with self.assertRaises(KeyError):
            book.get(b.ref)

    def test_a_hold_confirmed_in_time_becomes_a_booking(self):
        book, clock = make()
        b = book.book("S1", "Ada", vehicle=True)
        clock.advance(10)
        self.assertEqual(book.confirm(b.ref).status, "confirmed")

    def test_a_lapsed_hold_cannot_be_confirmed(self):
        book, clock = make()
        b = book.book("S1", "Ada", vehicle=True)
        clock.advance(20)
        book.available_cars("S1")
        with self.assertRaises(HoldExpired):
            book.confirm(b.ref)

    def test_a_lapsed_hold_goes_to_the_waitlist(self):
        book, clock = make(car_spaces=1)
        book.book("S1", "Ada", vehicle=True)
        book.waitlist("S1", "Bo", vehicle=True)
        clock.advance(20)
        book.available_cars("S1")
        with self.assertRaises(FullError):
            book.book("S1", "Cy", vehicle=True)

    def test_a_second_hold_replaces_the_first(self):
        book, _ = make(car_spaces=1)
        book.book("S1", "Ada", vehicle=True)
        second = book.book("S1", "Ada", vehicle=True)
        self.assertEqual(book.get(second.ref).status, "held")
        with self.assertRaises(FullError):
            book.book("S1", "Bo", vehicle=True)

    def test_holds_survive_a_restart(self):
        book, clock = make()
        b = book.book("S1", "Ada", vehicle=True)
        path = os.path.join(tempfile.mkdtemp(), "holds.json")
        book.save_holds(path)
        restarted = BookingBook([sailing(car_spaces=2)], hold_minutes=15, clock=clock)
        restarted.load_holds(path)
        self.assertEqual(restarted.get(b.ref).status, "held")

    def test_the_desk_places_and_confirms(self):
        book, _ = make()
        desk = HoldDesk(book)
        b = desk.place("S1", "Ada", vehicle=True)
        self.assertEqual(desk.confirm(b.ref).status, "confirmed")

    def test_the_hold_fee_is_a_tenth_of_the_fare(self):
        self.assertEqual(pricing.hold_fee(42000), 4200)


if __name__ == "__main__":
    unittest.main()
