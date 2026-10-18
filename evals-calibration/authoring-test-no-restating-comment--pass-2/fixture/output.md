from datetime import datetime

from roastlog.log import Roast
from roastlog.report import development_ratio


def roast(first_crack, dropped):
    return Roast(
        "L-2291",
        datetime(2026, 10, 14, 9, 0),
        1000,
        dropped_at=dropped,
        first_crack_at=first_crack,
    )


def test_a_ratio_with_a_fraction_is_floored_not_rounded():
    # 100 s of development in a 600 s roast is 16.67%, which rounds up but floors down.
    assert development_ratio(
        roast(datetime(2026, 10, 14, 9, 8, 20), datetime(2026, 10, 14, 9, 10))
    ) == 16


def test_a_roast_without_a_first_crack_has_no_ratio():
    assert development_ratio(roast(None, datetime(2026, 10, 14, 9, 10))) is None


def test_a_roast_that_was_never_dropped_has_no_ratio():
    assert development_ratio(roast(datetime(2026, 10, 14, 9, 8, 20), None)) is None
