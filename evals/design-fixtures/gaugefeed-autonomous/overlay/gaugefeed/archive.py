"""Packs a month of saved cycle documents into one archive for the records office."""

import json
import sys
from pathlib import Path


def pack_month(document_dir: str, month: str) -> str:
    """Return one JSON archive of the documents saved in document_dir for month (YYYY-MM).

    Cron saves each cycle's document as <cycle time>.json; they are archived as
    they were printed, in cycle order.
    """
    paths = sorted(Path(document_dir).glob(f"{month}-*.json"))
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    return json.dumps({"month": month, "cycles": documents}, indent=2)


def main(argv: list[str]) -> int:
    """Print the archive of the month named in argv; return the exit status."""
    if len(argv) != 3:
        print("usage: python -m gaugefeed.archive DOCUMENT_DIR YYYY-MM", file=sys.stderr)
        return 2
    print(pack_month(argv[1], argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
