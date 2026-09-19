"""AllocationEngine: turns reservations into bin assignments.

See GLOSSARY.md, "AllocationEngine".
"""

from .models import OrderLineStatus


class AllocationEngine:
    def allocate(self, db, line):
        """Assign specific bins (and lots) to a reserved order line.

        Bins are taken earliest-expiry first; quarantine bins are skipped.
        Returns the pick tasks, one per bin used.
        """
        tasks = []
        remaining = line.qty
        for row in db.bins_for(line.sku, order_by="expires", quarantine=False):
            take = min(row.qty, remaining)
            tasks.append(db.new_pick_task(line, row.bin, row.lot_no, take))
            remaining -= take
            if remaining == 0:
                break
        line.status = OrderLineStatus.ALLOCATED
        return tasks
