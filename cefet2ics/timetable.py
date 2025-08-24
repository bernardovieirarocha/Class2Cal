import datetime
from typing import Tuple

WEEKDAY_MAP = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4}

def first_occurrence(start_date: datetime.date, weekday: str) -> datetime.date:
    wd = WEEKDAY_MAP[weekday]
    days_ahead = (wd - start_date.weekday() + 7) % 7
    return start_date + datetime.timedelta(days=days_ahead)

def format_dt(date: datetime.date, time: str) -> str:
    return f"{date.strftime('%Y%m%d')}T{time.replace(':','')}00"
