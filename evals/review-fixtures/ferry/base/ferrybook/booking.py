from dataclasses import dataclass


class FullError(Exception):
    pass


@dataclass
class Booking:
    ref: int
    sailing_id: str
    passenger: str
    vehicle: bool


class BookingBook:
    """The bookings for a set of sailings, in memory."""

    def __init__(self, sailings, reserved_car_spaces=0):
        self._sailings = {s.id: s for s in sailings}
        self._reserved = reserved_car_spaces
        self._bookings = {}
        self._next_ref = 1

    def book(self, sailing_id, passenger, vehicle=False):
        if vehicle and self.available_cars(sailing_id) <= 0:
            raise FullError(sailing_id)
        if not vehicle and self.available_foot(sailing_id) <= 0:
            raise FullError(sailing_id)
        booking = Booking(self._next_ref, sailing_id, passenger, vehicle)
        self._next_ref += 1
        self._bookings[booking.ref] = booking
        return booking

    def cancel(self, ref):
        del self._bookings[ref]

    def get(self, ref):
        return self._bookings[ref]

    def available_cars(self, sailing_id):
        """Car spaces that can still be sold on the sailing."""
        taken = sum(1 for b in self._bookings.values() if b.sailing_id == sailing_id and b.vehicle)
        return self._sailings[sailing_id].car_spaces - self._reserved - taken

    def available_foot(self, sailing_id):
        taken = sum(1 for b in self._bookings.values() if b.sailing_id == sailing_id and not b.vehicle)
        return self._sailings[sailing_id].foot_spaces - taken


def make_book(sailings, settings):
    return BookingBook(sailings, reserved_car_spaces=settings["reserved_car_spaces"])
