"""Fares, in integer øre (ADR-0002)."""

ROUTES = {
    "ARD-SKO": {"car": 42000, "foot": 9500},
    "SKO-HUS": {"car": 31000, "foot": 7000},
}


def car_fare(route, book, sailing_id, settings):
    fare = ROUTES[route]["car"]
    if book.available_cars(sailing_id) < settings["surge_threshold"]:
        fare += fare * settings["surge_percent"] // 100
    return fare


def foot_fare(route):
    return ROUTES[route]["foot"]


def child_fare(route):
    return int(foot_fare(route) * 0.5)
