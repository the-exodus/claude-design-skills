"""Picking: the pick queue and pick lists.

Pick tasks enter the pick queue when their wave is released. The pick
queue is not first-in-first-out: tasks are ordered by wave, then by walk
sequence through the zone.
"""

import heapq


class PickQueue:
    def __init__(self):
        self._heap = []

    def push(self, task):
        heapq.heappush(self._heap, (task.wave_id, task.walk_seq, task.id, task))

    def pop(self):
        return heapq.heappop(self._heap)[3]


class PickListBuilder:
    """Builds one pick list per picker per zone from the pick queue.

    See GLOSSARY.md: PickListBuilder.
    """

    def build(self, queue, zone, size):
        picks = []
        while len(picks) < size and queue:
            task = queue.pop()
            if task.zone == zone:
                picks.append(task)
        return picks
