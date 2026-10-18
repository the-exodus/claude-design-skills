import json
import time
from dataclasses import asdict, dataclass


class FullError(Exception):
    pass


class HoldExpired(Exception):
    pass


@dataclass
class Booking:
    ref: int
    sailing_id: str
    passenger: str
    vehicle: bool
    status: str = "held"
    held_until: float = 0.0


class BookingBook:
    """The bookings for a set of sailings, in memory.

    A booking starts as a hold and becomes confirmed with confirm(). Lapsed
    holds are settled at the start of each operation (ADR-0003).
    """

    def __init__(self, sailings, reserved_car_spaces=0, hold_minutes=30, clock=time.monotonic):
        self._sailings = {s.id: s for s in sailings}
        self._reserved = reserved_car_spaces
        self._hold_seconds = hold_minutes * 60
        self._clock = clock
        self._bookings = {}
        self._waitlist = {}

    def _new_ref(self):
        # Keep references short: a settled hold gives its number back.
        return max(self._bookings, default=0) + 1

    def _settle(self):
        now = self._clock()
        for ref, b in list(self._bookings.items()):
            if b.status == "held" and b.held_until <= now:
                del self._bookings[ref]
                self._promote(b.sailing_id)

    def _promote(self, sailing_id):
        queue = self._waitlist.get(sailing_id)
        if queue:
            passenger, vehicle = queue.pop(0)
            self._place(sailing_id, passenger, vehicle)

    def _place(self, sailing_id, passenger, vehicle):
        booking = Booking(self._new_ref(), sailing_id, passenger, vehicle, "held", self._clock() + self._hold_seconds)
        self._bookings[booking.ref] = booking
        return booking

    def _taken(self, sailing_id, vehicle, statuses):
        return sum(
            1
            for b in self._bookings.values()
            if b.sailing_id == sailing_id and b.vehicle == vehicle and b.status in statuses
        )

    def book(self, sailing_id, passenger, vehicle=False):
        """Places a hold. A passenger's earlier hold on the sailing is replaced."""
        self._settle()
        for ref, b in list(self._bookings.items()):
            if b.sailing_id == sailing_id and b.passenger == passenger and b.status == "held":
                del self._bookings[ref]
        sailing = self._sailings[sailing_id]
        if vehicle:
            free = sailing.car_spaces - self._reserved - self._taken(sailing_id, True, ("held", "confirmed"))
        else:
            free = sailing.foot_spaces - self._taken(sailing_id, False, ("held", "confirmed"))
        if free <= 0:
            raise FullError(sailing_id)
        return self._place(sailing_id, passenger, vehicle)

    def confirm(self, ref):
        booking = self._bookings.get(ref)
        if booking is None:
            raise HoldExpired(ref)
        booking.status = "confirmed"
        return booking

    def extend_hold(self, ref, minutes):
        self._settle()
        self._bookings[ref].held_until += minutes * 60

    def waitlist(self, sailing_id, passenger, vehicle=False):
        self._waitlist.setdefault(sailing_id, []).append((passenger, vehicle))

    def cancel(self, ref):
        self._settle()
        booking = self._bookings.pop(ref)
        self._promote(booking.sailing_id)

    def get(self, ref):
        self._settle()
        return self._bookings[ref]

    def available_cars(self, sailing_id):
        """Car spaces a customer could still get: held spaces may yet be released."""
        self._settle()
        confirmed = self._taken(sailing_id, True, ("confirmed",))
        return self._sailings[sailing_id].car_spaces - self._reserved - confirmed

    def available_foot(self, sailing_id):
        self._settle()
        return self._sailings[sailing_id].foot_spaces - self._taken(sailing_id, False, ("held", "confirmed"))

    def save_holds(self, path):
        """Writes the open holds, so that they survive a restart (see assumptions.md, A2)."""
        self._settle()
        held = [asdict(b) for b in self._bookings.values() if b.status == "held"]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(held, f)

    def load_holds(self, path):
        with open(path, encoding="utf-8") as f:
            for row in json.load(f):
                booking = Booking(**row)
                self._bookings[booking.ref] = booking


def make_book(sailings, settings):
    return BookingBook(sailings, reserved_car_spaces=settings["reserved_car_spaces"])
