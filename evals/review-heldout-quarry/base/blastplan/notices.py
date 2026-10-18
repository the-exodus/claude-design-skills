"""Neighbour notices: one plain-text file per receptor per blast, in the outbox."""

import os
from pathlib import Path

NOTICE = """To: {name}
Blast {blast_id} on bench {bench} is planned for {local:%A %d %B %Y at %H:%M} ({zone}).
Please keep clear of the quarry boundary for fifteen minutes either side.
Issued {issued:%Y-%m-%d %H:%M} UTC.
"""


class NoticeError(Exception):
    pass


def notice_path(outbox, blast_id, receptor_id):
    return Path(outbox) / f"notice-{blast_id}-{receptor_id}.txt"


def notice_lead(blast, issued_at):
    """Hours of notice a receptor gets if notified at `issued_at`."""
    return (blast.scheduled_at - issued_at).total_seconds() / 3600


def _write_atomic(path, text):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.rename(tmp, path)


def issue_notices(blast, cfg, now):
    """Write a notice for every receptor and return the paths written."""
    if notice_lead(blast, now) < cfg.notice_hours:
        raise NoticeError(
            f"blast {blast.id} is less than {cfg.notice_hours} hours away; too late to notify"
        )
    outbox = Path(cfg.outbox)
    outbox.mkdir(parents=True, exist_ok=True)
    paths = []
    for receptor in cfg.receptors:
        path = notice_path(outbox, blast.id, receptor.id)
        if path.exists():
            raise NoticeError(f"{path.name} has already been issued")
        text = NOTICE.format(
            name=receptor.name,
            blast_id=blast.id,
            bench=blast.bench,
            local=blast.scheduled_at.astimezone(cfg.zone),
            zone=cfg.site_timezone,
            issued=now,
        )
        _write_atomic(path, text)
        paths.append(path)
    return paths
