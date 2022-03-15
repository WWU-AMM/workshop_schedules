from typing import Optional

from attr import define, field

import datetime, time

from workshop_schedules.tools import duration_to_date


@define
class Slot:
    start: datetime.datetime
    end: datetime.datetime
    talks: list[dict] = field(init=False, factory=list)
    pause: Optional[dict] = field(init=False, factory=None)

    @property
    def duration(self) -> datetime.timedelta:
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
        return [s.get("name", None) or s.get("description") for s in self._parallel_sessions]

    def add_session(self, session: dict) -> None:

        slots = []
        start = self.start
        if 'pause' in session.keys():
            slots = [Slot(start, start + duration_to_date(session["pause"]))]
        else:
            for talk in session['talks']:
                end = start + duration_to_date(talk["duration"])
                slots.append(Slot(start, end))
        if self.slots:
            assert all(s.start == p.start for s, p in zip(slots, self.slots)), "Slots must agree for parallel sessions"
            assert all(s.end == p.end for s, p in zip(slots, self.slots)), "Slots must agree for parallel sessions"
        self._parallel_sessions.append(session)
        for i, slot in enumerate(slots):
            for sess in self._parallel_sessions:
                try:
                    event = sess["talks"][i]
                    slot.talks.append(event)
                except KeyError:
                    assert "pause" in sess
                    slot.pause = sess["pause"]
        self.slots = slots
        self.end = self.slots[-1].end
