"""Batch jobs and the job queue.

Nightly batch jobs (lapse expired reservations, refresh the SKU cache) are
pushed onto the job queue and run first-in-first-out by the worker.
"""

from collections import deque

NIGHTLY_BATCH = ["lapse_expired_reservations", "refresh_sku_cache"]


class JobQueue:
    def __init__(self):
        self._jobs = deque()

    def enqueue(self, job):
        self._jobs.append(job)

    def next(self):
        return self._jobs.popleft()
