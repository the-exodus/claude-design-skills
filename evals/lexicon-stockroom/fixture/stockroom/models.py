"""Core stock records: SKUs, bins, lots and movements."""

from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass
class Sku:
    """A stock-keeping unit: one sellable product variant."""

    code: str
    description: str


@dataclass
class Bin:
    """The smallest addressable storage location."""

    code: str
    zone: str
    quarantine: bool = False


@dataclass
class StockLot:
    """Units of one SKU received together, sharing an expiry date.

    Called StockLot rather than Batch because "batch" already means a
    batch job in jobs.py. See GLOSSARY.md: StockLot.
    """

    sku: str
    lot_no: str
    expires: date | None


class MovementKind(Enum):
    RECEIPT = "receipt"        # from a supplier or a customer; no source bin
    PUTAWAY = "putaway"
    TRANSFER = "transfer"
    PICK = "pick"              # to an order; no destination bin
    ADJUSTMENT = "adjustment"  # on-hand corrected after a count; nothing moves


@dataclass
class Movement:
    kind: MovementKind
    sku: str
    qty: int
    from_bin: str | None
    to_bin: str | None
    lot_no: str | None = None


class OrderLineStatus(Enum):
    OPEN = "open"
    RESERVED = "reserved"
    BACKORDERED = "backordered"  # accepted with nothing available to reserve
    ALLOCATED = "allocated"
    PICKED = "picked"
