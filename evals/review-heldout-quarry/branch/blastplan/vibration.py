"""Predicted ground vibration at the nearest receptor.

Uses the site law PPV = k * (D / sqrt(W)) ** -b, with D the distance in
metres, W the maximum instantaneous charge in kg, and k, b fitted to this
site's monitoring records.
"""

import math


def predict_ppv(charge_kg, distance_m, cfg):
    """Predicted peak particle velocity in mm/s, rounded up to 0.1 mm/s.

    Rounding up keeps a prediction of 6.01 from passing a 6.0 limit.
    """
    scaled = distance_m / math.sqrt(charge_kg)
    ppv = cfg.site_k * scaled ** (-cfg.site_b)
    return math.ceil(ppv * 10) / 10


def within_limit(charge_kg, distance_m, cfg):
    return predict_ppv(charge_kg, distance_m, cfg) <= cfg.ppv_limit_mm_s
