#!/usr/bin/env python3

import collections
from pprint import pprint
import datetime, time
from attr import define, field
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import humanfriendly

fn = "program.yml"

with open(fn, "rt") as yml:
    data = load(yml, Loader=Loader)


@define
class Slot:
    start: datetime.datetime
    end: datetime.datetime

    @property
    def duration(self)->datetime.timedelta:
        return self.end - self.start


def duration_to_date(duration: str) -> datetime.timedelta:
    seconds = humanfriendly.parse_timespan(duration)
    return datetime.timedelta(seconds=seconds)


@define
class Block:
    _parallel_sessions: list[dict] = field(init=False, factory=list)
    slots: list[Slot] = field(init=False, factory=list)
    start: datetime.datetime
    end: datetime.datetime = field()

    @end.default
    def _end(self) -> datetime.datetime:
        return self.start

    @property
    def session_count(self) -> int:
        return len(self._parallel_sessions)

    @property
    def first_session(self) -> dict:
        return self._parallel_sessions[0]

    @property
    def name(self):
        return [
            s.get("name", None) or s.get("description") for s in self._parallel_sessions
        ]

    def add_session(self, session:dict) -> None:

        slots = []
        start = self.start
        if 'pause' in session.keys():
            slots = [Slot(start, start+duration_to_date(session["pause"]))]
        else:
            for talk in session['talks']:
                end = start + duration_to_date(talk["duration"])
                slots.append(Slot(start, end))
        if self.slots:
            assert all(
                s == p for s, p in zip(slots, self.slots)
            ), "Slots must agree for parallel sessions"
        else:
            self.slots = slots
        self.end = self.slots[-1].end
        self._parallel_sessions.append(session)


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
