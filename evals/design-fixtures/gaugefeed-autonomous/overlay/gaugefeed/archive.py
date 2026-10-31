"""Packs a month of gauge logger dumps into one archive for the records office."""

import csv
import json
import sys
from pathlib import Path


def read_dump(path: Path) -> list[list]:
    """Return the dump's entries, each [logged time, level in metres], as logged."""
    with path.open(encoding="utf-8", newline="") as dump:
        return [[logged, float(level)] for logged, level in csv.reader(dump)]


def pack_month(dump_dir: str, month: str) -> str:
    """Return one JSON archive of the logger dumps in dump_dir for month (YYYY-MM).

    Field staff save each gauge's dump as <gauge>-<YYYY-MM>.csv; the archive keeps
    every entry as logged, keyed by gauge.
    """
    suffix = f"-{month}.csv"
    gauges = {
        path.name[: -len(suffix)]: read_dump(path)
        for path in sorted(Path(dump_dir).glob(f"*{suffix}"))
    }
    return json.dumps({"month": month, "gauges": gauges}, indent=2)


def main(argv: list[str]) -> int:
    """Print the archive of the month named in argv; return the exit status."""
    if len(argv) != 3:
        print("usage: python -m gaugefeed.archive DUMP_DIR YYYY-MM", file=sys.stderr)
        return 2
    print(pack_month(argv[1], argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
