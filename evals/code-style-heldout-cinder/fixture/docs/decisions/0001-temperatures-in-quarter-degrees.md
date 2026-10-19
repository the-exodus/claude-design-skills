# 0001. Temperatures are integer quarter-degrees

Status: Accepted

The amplifier reports the hot junction in steps of 0.25 °C. We carry every
temperature as an integer count of those steps (`QuarterDegrees`) rather than as
a float, so comparisons against targets are exact and there is no rounding to
reason about. Floats do not cross module boundaries.
