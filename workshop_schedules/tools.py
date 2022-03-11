import humanfriendly
import datetime

def duration_to_date(duration: str) -> datetime.timedelta:
    seconds = humanfriendly.parse_timespan(duration)
    return datetime.timedelta(seconds=seconds)
