
from attr import define, field

import datetime, time

from workshop_schedules.tools import duration_to_date


@define
class Slot:
    start: datetime.datetime
    end: datetime.datetime

    @property
    def duration(self)->datetime.timedelta:
        return self.end - self.start



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
