from datetime import datetime, timezone

from ferrybook.schedule import Sailing


def sailing(id="S1", route="ARD-SKO", car_spaces=10, foot_spaces=50, departs="2026-06-01T07:30:00", arrives="2026-06-01T08:10:00"):
    return Sailing(
        id=id,
        route=route,
        departs=datetime.fromisoformat(departs).replace(tzinfo=timezone.utc),
        arrives=datetime.fromisoformat(arrives).replace(tzinfo=timezone.utc),
        car_spaces=car_spaces,
        foot_spaces=foot_spaces,
    )
