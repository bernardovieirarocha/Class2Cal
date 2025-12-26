import datetime

WEEKDAY_MAP = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4}

def first_occurrence(start_date: datetime.date, weekday: str) -> datetime.date:
    """Finds the first date of a given weekday on or after the start_date."""
    wd = WEEKDAY_MAP.get(weekday, 0)
    days_ahead = (wd - start_date.weekday() + 7) % 7
    return start_date + datetime.timedelta(days=days_ahead)

def format_dt(date: datetime.date, time: str) -> str:
    """Formats date and time into iCalendar string format (YYYYMMDDTHHMMSS)."""
    return f"{date.strftime('%Y%m%d')}T{time.replace(':','')}00"

def ics_escape(text: str) -> str:
    """Escapes special characters for iCalendar format."""
    if not text:
        return ""
    return str(text).replace('\\', '\\\\').replace(',', '\\,').replace(';', '\\;').replace('\n', '\\n')
