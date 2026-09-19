"""Counting on-hand: cycle counts and stocktakes.

A cycle count covers one bin and runs while picking carries on; only that
bin is locked, for the minutes the count takes. A stocktake covers every
bin and needs picking stopped.
"""

from .models import Movement, MovementKind
from .movements import post_movement


def post_count(db, bin_code, sku, counted):
    """Post an adjustment for the difference between counted and on-hand."""
    on_hand = db.sum_ledger(bin_code, sku)
    diff = counted - on_hand
    if diff == 0:
        return None
    movement = Movement(MovementKind.ADJUSTMENT, sku, diff, None, bin_code)
    return post_movement(db, movement)
