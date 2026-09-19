"""Availability: what can still be promised to a new order."""

AVAILABLE_SQL = """
SELECT COALESCE(SUM(l.qty), 0)
       - (SELECT COALESCE(SUM(r.qty), 0) FROM reservations r
          WHERE r.sku = :sku AND r.lapsed = false)
FROM ledger l JOIN bins b ON b.code = l.bin
WHERE l.sku = :sku AND b.quarantine = false
"""


def available_qty(db, sku):
    """Return the available quantity of ``sku`` across the warehouse.

    Sums the bin rows and subtracts open reservations in a single query.
    Quarantine bins are left out of the sum.
    """
    return db.scalar(AVAILABLE_SQL, {"sku": sku})
