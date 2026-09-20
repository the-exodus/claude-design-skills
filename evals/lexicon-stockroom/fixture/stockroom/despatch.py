"""Despatch: handing packed shipments to the carrier."""

from datetime import datetime, timezone


class CollectionDesk:
    """Records a carrier collection.

    See GLOSSARY.md: CollectionDesk.
    """

    def __init__(self, db):
        self.db = db

    def sign_off(self, collection_ref, signed_by, shipment_ids):
        """Mark shipments despatched once the carrier's driver has signed."""
        now = datetime.now(timezone.utc)
        for shipment_id in shipment_ids:
            self.db.execute(
                "UPDATE shipments SET despatched_at = :now, signed_by = :who, "
                "collection_ref = :ref WHERE id = :id",
                {"now": now, "who": signed_by, "ref": collection_ref, "id": shipment_id},
            )
