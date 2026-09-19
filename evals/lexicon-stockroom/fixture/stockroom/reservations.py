"""Reservations: quantity set aside for an order line, not tied to a bin.

A reservation lapses after ``reservation_ttl`` (stockroom.toml) unless its
order line is allocated first.
"""

from datetime import datetime, timedelta

from . import events
from .availability import available_qty
from .db import uow
from .models import OrderLineStatus


class ReservationService:
    """Creates and lapses reservations. See GLOSSARY.md: ReservationService."""

    def __init__(self, reservation_ttl: timedelta):
        self.reservation_ttl = reservation_ttl

    def reserve(self, line):
        """Set ``line.qty`` aside, or backorder the line if too little is available."""
        with uow() as db:
            if available_qty(db, line.sku) < line.qty:
                line.status = OrderLineStatus.BACKORDERED
                return None
            line.status = OrderLineStatus.RESERVED
            expires = datetime.now() + self.reservation_ttl
            return db.add_reservation(line, expires=expires)

    def lapse_expired(self):
        with uow() as db:
            for reservation in db.expired_reservations(datetime.now()):
                reservation.lapsed = True
                events.publish("ReservationLapsed", reservation=reservation)
