from datetime import datetime

from roastlog.log import Roast
from roastlog.report import development_ratio


def at(hour, minute, second=0):
    return datetime(2026, 10, 14, hour, minute, second)


def roast(first_crack, dropped):
    return Roast(
        "L-2291",
        at(9, 0),
        1000,
        dropped_at=dropped,
        first_crack_at=first_crack,
    )


def test_development_ratio_floors_rather_than_rounds():
    # 124 s of development in a 600 s roast is 20.67%, which rounds up to 21.
    assert development_ratio(roast(at(9, 7, 56), at(9, 10))) == 20


def test_a_roast_without_a_first_crack_has_no_development_ratio():
    assert development_ratio(roast(None, at(9, 10))) is None


def test_an_undropped_roast_has_no_development_ratio():
    assert development_ratio(roast(at(9, 7, 56), None)) is None
