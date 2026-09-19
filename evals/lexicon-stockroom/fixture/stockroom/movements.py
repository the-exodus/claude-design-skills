"""Posting stock movements.

The reconciliation sweep: inside every movement's unit of work the source
bin's on-hand is re-summed from the ledger, and the movement is rejected
if it would take on-hand below zero (ADR-0003).
"""

from . import events


class NegativeOnHand(Exception):
    pass


def post_movement(db, movement):
    if movement.from_bin is not None:
        on_hand = db.sum_ledger(movement.from_bin, movement.sku)
        if on_hand - movement.qty < 0:
            raise NegativeOnHand(movement)
    db.append_ledger(movement)
    events.publish("StockMoved", movement=movement)
    return movement
