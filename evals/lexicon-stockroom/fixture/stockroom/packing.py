"""Packing slips.

A packing slip is printed for every shipment and lists the SKUs, lots and
quantities in the box.
"""

from dataclasses import dataclass, field


@dataclass
class PackingSlip:
    shipment_id: str
    lines: list = field(default_factory=list)


def print_packing_slip(shipment):
    slip = PackingSlip(shipment.id)
    for line in shipment.lines:
        slip.lines.append((line.sku, line.lot_no, line.qty))
    return slip
