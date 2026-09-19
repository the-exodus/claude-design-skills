"""Customer returns.

Returned units are received into a quarantine bin and inspected before
they can be reserved again.
"""

from .models import Movement, MovementKind
from .movements import post_movement


def receive_return(db, order_line, qty, quarantine_bin):
    movement = Movement(MovementKind.RECEIPT, order_line.sku, qty, None, quarantine_bin)
    return post_movement(db, movement)
