"""Command line for the shotfirer and the site office."""

import argparse
import sys
from datetime import datetime, timezone

from . import config, notices, store
from .models import Blast
from .notices import NoticeError
from .rescheduler import Rescheduler
from .schedule import PostponeLimitError, ScheduleError


def _parse_local(text, cfg):
    naive = datetime.strptime(text, "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=cfg.zone).astimezone(timezone.utc)


def _local(when, cfg):
    return f"{when.astimezone(cfg.zone):%a %d %b %Y %H:%M}"


def build_parser():
    parser = argparse.ArgumentParser(prog="blastplan")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="plan a blast")
    add.add_argument("blast_id")
    add.add_argument("bench")
    add.add_argument("at", help="site local time, YYYY-MM-DD HH:MM")
    add.add_argument("--charge", type=float, required=True, help="kg per delay")
    add.add_argument("--distance", type=float, required=True, help="metres to nearest receptor")
    sub.add_parser("cancel", help="cancel a blast").add_argument("blast_id")
    sub.add_parser("notify", help="write neighbour notices").add_argument("blast_id")
    postpone = sub.add_parser("postpone", help="move a planned blast to a later time")
    postpone.add_argument("blast_id")
    postpone.add_argument("--to", help="site local time, YYYY-MM-DD HH:MM (default: next free slot)")
    sub.add_parser("list", help="show the schedule")
    sub.add_parser("status", help="notice lead for planned blasts")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = config.load()
    now = datetime.now(timezone.utc)
    schedule = store.load(cfg.schedule_file, cfg)
    try:
        if args.command == "add":
            blast = Blast(args.blast_id, args.bench, _parse_local(args.at, cfg),
                          args.charge, args.distance)
            schedule.add(blast)
            store.save(schedule, cfg.schedule_file)
            print(f"{blast.id} planned for {_local(blast.scheduled_at, cfg)}")
        elif args.command == "cancel":
            schedule.cancel(args.blast_id)
            store.save(schedule, cfg.schedule_file)
            print(f"{args.blast_id} cancelled")
        elif args.command == "notify":
            for path in notices.issue_notices(schedule.get(args.blast_id), cfg, now):
                print(path)
        elif args.command == "postpone":
            new_time = _parse_local(args.to, cfg) if args.to else None
            rescheduler = Rescheduler(schedule)
            try:
                blast = rescheduler.postpone(args.blast_id, new_time, now)
            except PostponeLimitError as exc:
                schedule.cancel(args.blast_id)
                store.save(schedule, cfg.schedule_file)
                print(f"blastplan: {exc} (limit {rescheduler.limit}); "
                      f"{args.blast_id} has been cancelled", file=sys.stderr)
                return 2
            store.save(schedule, cfg.schedule_file)
            print(f"{blast.id} postponed to {_local(blast.scheduled_at, cfg)}")
        elif args.command == "list":
            for blast in schedule:
                print(f"{blast.id:6} {_local(blast.scheduled_at, cfg)}  {blast.bench:10} {blast.status}")
        elif args.command == "status":
            for blast in schedule:
                if blast.status != "planned" or blast.scheduled_at < now:
                    continue
                lead = notices.notice_lead(blast, now)
                flag = "  SHORT NOTICE" if lead < cfg.notice_hours else ""
                print(f"{blast.id:6} {lead:6.1f}h notice{flag}")
    except (ScheduleError, NoticeError) as exc:
        print(f"blastplan: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
