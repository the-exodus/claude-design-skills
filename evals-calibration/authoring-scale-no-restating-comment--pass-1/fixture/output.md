from . import serial_port

_GRAMS_PER_UNIT = {"g": 1.0, "kg": 1000.0}


class ScaleError(Exception):
    pass


def next_stable_weight_g(device: str = "/dev/ttyUSB0") -> float:
    """Return the next weight the scale settles on, in grams.

    Blocks until the scale sends a stable reading, which for a scale that has
    gone to sleep means until something moves on the pan.
    """
    frames = serial_port.lines(device)
    # The first frame after the scale wakes repeats the weight from before it
    # slept, whatever is on the pan now; an awake scale sends five a second, so
    # dropping one frame costs nothing either way.
    next(frames, None)
    for frame in frames:
        weight_g = _stable_weight_g(frame)
        if weight_g is not None:
            return weight_g
    raise ScaleError(f"{device} stopped sending frames")


def _stable_weight_g(frame: str) -> float | None:
    """The frame's weight in grams, or None if it is not a stable reading.

    A frame we cannot read counts as unstable rather than as an error: line
    noise is ordinary on the port, and the next frame is 200ms behind it.
    """
    fields = frame.split(",")
    if len(fields) != 3:
        return None
    status, _net_or_gross, reading = fields
    if status == "OL":
        raise ScaleError(f"scale over capacity: {frame}")
    if status != "ST":
        return None
    # The unit follows the front panel, which staff can change at any time.
    weight, _, unit = reading.partition(" ")
    try:
        return float(weight) * _GRAMS_PER_UNIT[unit]
    except (KeyError, ValueError):
        return None
