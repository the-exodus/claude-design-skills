"""API payloads: plain data transfer objects, no behaviour."""

from dataclasses import dataclass


@dataclass
class CycleCount:
    """Request body for POST /bins/{bin}/counts."""

    sku: str
    counted: int


@dataclass
class SkuOut:
    code: str
    description: str
    available: int
