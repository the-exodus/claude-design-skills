from . import serial_port

_GRAMS_PER_UNIT = {"g": 1.0, "kg": 1000.0}


class OverCapacity(Exception):
    """The pan is loaded past the scale's range, so it reports no weight."""


def stable_weight_g(device: str = "/dev/ttyUSB0") -> float:
    """Return the next weight the scale calls stable, in grams.

    Blocks while the reading settles, so load the pan before calling.
    """
    frames = serial_port.lines(device)
    # The first frame after the scale wakes is marked stable but repeats the
    # weight from before it slept, whatever is on the pan now.
    next(frames)
    for frame in frames:
        status, _, reading = frame.split(",")
        if status == "OL":
            raise OverCapacity(frame)
        if status != "ST":
            continue
        weight, unit = reading.split()
        # The unit follows the front panel, which staff can change at any time.
        return float(weight) * _GRAMS_PER_UNIT[unit]
