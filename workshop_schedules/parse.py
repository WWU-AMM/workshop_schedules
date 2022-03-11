#!/usr/bin/env python3

import collections
from pprint import pprint
import datetime, time
from yaml import load

from workshop_schedules.objects import Block

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



def parse_file(fn = "program.yml"):

    with open(fn, "rt") as yml:
        data = load(yml, Loader=Loader)






    for day in data["days"]:
        start = time.strptime(day["start"], "%H:%M")
        day["start"] = datetime.datetime.combine(
            day["date"], datetime.time(start.tm_hour, start.tm_min)
        )
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

            pprint(
                {
                    "name": current_block.name,
                    "sessions": current_block.session_count,
                    "end": current_block.end,
                    "start": current_block.start,
                }
            )

if __name__ == "__main__":
    parse_file()
