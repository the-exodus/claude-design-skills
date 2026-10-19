from datetime import datetime

from roastlog.log import Roast
from roastlog.report import weight_loss


def roast(green, roasted):
    return Roast("L-2291", datetime(2026, 10, 14, 9, 0), green, roasted_weight_g=roasted)


def test_weight_loss_is_a_share_of_the_green_weight():
    assert weight_loss(roast(1000, 850)) == 0.15


def test_an_unweighed_roast_has_no_weight_loss():
    assert weight_loss(roast(1000, None)) is None
