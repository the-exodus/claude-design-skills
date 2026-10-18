"""Neighbour notices: one plain-text file per receptor per blast, in the outbox."""

import os
from datetime import datetime, timezone
from pathlib import Path

NOTICE = """To: {name}
Blast {blast_id} on bench {bench} is planned for {local:%A %d %B %Y at %H:%M} ({zone}).
Please keep clear of the quarry boundary for fifteen minutes either side.
Issued {issued:%Y-%m-%d %H:%M} UTC.
"""

REVISED = """To: {name}
REVISED NOTICE: this replaces the earlier notice for blast {blast_id}.
Blast {blast_id} on bench {bench} has been moved to {local:%A %d %B %Y at %H:%M} ({zone}).
Please keep clear of the quarry boundary for fifteen minutes either side.
Issued {issued:%Y-%m-%d %H:%M} UTC.
"""


class NoticeError(Exception):
    pass


def notice_path(outbox, blast_id, receptor_id):
    return Path(outbox) / f"notice-{blast_id}-{receptor_id}.txt"


def notice_lead(blast, issued_at):
    """Minutes of notice a receptor gets if notified at `issued_at`."""
    return int((blast.scheduled_at - issued_at).total_seconds() // 60)


def notified_receptors(outbox, blast_id):
    """Ids of the receptors that hold a notice for `blast_id`."""
    prefix = f"notice-{blast_id}-"
    return sorted(p.stem[len(prefix):] for p in Path(outbox).glob(f"{prefix}*.txt"))


def _write_atomic(path, text):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.rename(tmp, path)


def issue_notices(blast, cfg, now):
    """Write a notice for every receptor and return the paths written."""
    if notice_lead(blast, now) < cfg.notice_hours * 60:
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


def issue_revised(blast, cfg):
    """Replace each existing notice for `blast` with a revised one."""
    issued = datetime.now(timezone.utc)
    names = {receptor.id: receptor.name for receptor in cfg.receptors}
    paths = []
    for receptor_id in notified_receptors(cfg.outbox, blast.id):
        path = notice_path(cfg.outbox, blast.id, receptor_id)
        text = REVISED.format(
            name=names.get(receptor_id, receptor_id),
            blast_id=blast.id,
            bench=blast.bench,
            local=blast.scheduled_at.astimezone(cfg.zone),
            zone=cfg.site_timezone,
            issued=issued,
        )
        _write_atomic(path, text)
        paths.append(path)
    return paths
