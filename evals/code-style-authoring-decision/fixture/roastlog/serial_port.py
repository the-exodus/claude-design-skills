from collections.abc import Iterator

import serial  # pyserial


def lines(device: str = "/dev/ttyUSB0") -> Iterator[str]:
    """Yield the scale's frames as text, one per line, without the line ending."""
    with serial.Serial(device, 9600, timeout=2) as port:
        while True:
            raw = port.readline()
            if raw:
                yield raw.decode("ascii").rstrip("\r\n")
