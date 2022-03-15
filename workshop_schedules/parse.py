#!/usr/bin/env python3

import collections
import datetime, time
from pathlib import Path
from typing import List

from yaml import load

from workshop_schedules import output
from workshop_schedules.objects import Block

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def parse_file(fn: Path) -> List[dict]:

    with open(fn, "rt") as yml:
        data = load(yml, Loader=Loader)

    days = []
    for day in data["days"]:
        start = time.strptime(day["start"], "%H:%M")
        day["start"] = datetime.datetime.combine(day["date"], datetime.time(start.tm_hour, start.tm_min))
        day["blocks"] = []
        sessions = collections.deque(day["sessions"])

        current_block = None
        while sessions:
            start = current_block.end if current_block else day["start"]
            current_block = Block(start)
            current_block.add_session(sessions.popleft())
            if current_block.first_session.get("parallel", False):
                while sessions and sessions[-1].get("parallel", False):
                    current_block.add_session(sessions.popleft())
            day["blocks"].append(current_block)
        day["max_parallel_sessions"] = max((bl.session_count for bl in day["blocks"]))
        days.append(day)
    return days


if __name__ == "__main__":
    days = parse_file()
    for i, day in enumerate(days):
        output.write_day(day, filename=Path(f'day_{i+1}.html'))
