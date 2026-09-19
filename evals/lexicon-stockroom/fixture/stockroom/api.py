"""HTTP endpoints.

The SKU endpoint exposes ``available``, the figure sales staff look at.
"""

from .availability import available_qty
from .counting import post_count
from .db import uow
from .schemas import CycleCount, SkuOut


def get_sku(code):
    with uow() as db:
        sku = db.get_sku(code)
        return SkuOut(sku.code, sku.description, available_qty(db, code))


def post_bin_count(bin_code, body: CycleCount):
    with uow() as db:
        return post_count(db, bin_code, body.sku, body.counted)


def release_wave(wave_id, pick_queue):
    with uow() as db:
        for task in db.tasks_for_wave(wave_id):
            pick_queue.push(task)
