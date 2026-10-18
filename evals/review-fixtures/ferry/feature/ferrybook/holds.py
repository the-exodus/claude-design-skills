"""Front-desk operations on holds."""


class HoldDesk:
    def __init__(self, book):
        self._book = book

    def place(self, sailing_id, passenger, vehicle=False):
        return self._book.book(sailing_id, passenger, vehicle)

    def confirm(self, ref):
        return self._book.confirm(ref)

    def extend(self, ref, minutes):
        return self._book.extend_hold(ref, minutes)

    def cancel(self, ref):
        return self._book.cancel(ref)
