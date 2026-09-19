"""In-process event bus.

Modules publish StockMoved and ReservationLapsed; subscribers are called
synchronously, inside the publisher's unit of work.
"""

from collections import defaultdict

_subscribers = defaultdict(list)


def subscribe(event_name, handler):
    _subscribers[event_name].append(handler)


def publish(event_name, **payload):
    for handler in _subscribers[event_name]:
        handler(**payload)
