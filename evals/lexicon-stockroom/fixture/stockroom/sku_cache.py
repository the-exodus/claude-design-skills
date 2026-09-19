"""SkuCache: in-memory SKU records, refreshed every five minutes.

See the SkuCache entry in GLOSSARY.md.
"""

import time

from .db import uow
from .models import Sku


class SkuCache:
    TTL_SECONDS = 300

    def __init__(self):
        self._skus = {}
        self._loaded = 0.0

    def get(self, code):
        if time.monotonic() - self._loaded > self.TTL_SECONDS:
            self._refresh()
        return self._skus.get(code)

    def _refresh(self):
        with uow() as db:
            self._skus = {s.code: s for s in db.query(Sku)}
        self._loaded = time.monotonic()
