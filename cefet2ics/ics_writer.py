from typing import List, Dict, Optional
import datetime
from cefet2ics.cefet_code import parse_cefet_codes
from cefet2ics.timetable import first_occurrence, format_dt

def ics_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace(',', '\\,').replace(';', '\\;').replace('\n', '\\n')

def write_ics(courses: List[Dict], start: datetime.date, end: datetime.date, cal_name: str, out_path: str, exdates: Optional[str]=None) -> int:
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//bernardo//cefet-schedule//PT-BR',
        'CALSCALE:GREGORIAN',
        f'X-WR-CALNAME:{ics_escape(cal_name)}',
        'X-WR-TIMEZONE:America/Sao_Paulo'
    ]
    counter = 1
    n_events = 0
    for course in courses:
        alias = course.get('alias','')
        full_name = course.get('full_name','')
        professor = course.get('professor','')
        room = course.get('room','')
        schedule_codes = course.get('schedule_codes','')
        code_infos = parse_cefet_codes(schedule_codes)
        for info in code_infos:
            if 'error' in info:
                continue
            days = info['days']
            start_time = info['start_time']
            end_time = info['end_time']
            for day in days:
                dt = first_occurrence(start, day)
                dtstart = format_dt(dt, start_time)
                dtend = format_dt(dt, end_time)
                until = end.strftime('%Y%m%d') + 'T235959Z'
                rrule = f'FREQ=WEEKLY;BYDAY={day};UNTIL={until}'
                desc = f"{ics_escape(full_name)}\\nProfessor: {ics_escape(professor)}\\nSala: {ics_escape(room)}\\nCódigos: {ics_escape(schedule_codes)}"
                event = [
                    'BEGIN:VEVENT',
                    f'UID:{counter}@bernardo-cefet',
                    f'SUMMARY:{ics_escape(alias)}',
                    f'DESCRIPTION:{desc}',
                    f'LOCATION:{ics_escape(room)}',
                    f'DTSTART;TZID=America/Sao_Paulo:{dtstart}',
                    f'DTEND;TZID=America/Sao_Paulo:{dtend}',
                    f'RRULE:{rrule}'
                ]
                if exdates:
                    for exd in exdates.split(','):
                        try:
                            exd_dt = datetime.datetime.strptime(exd.strip(), '%Y-%m-%d').date()
                            exdate_str = format_dt(exd_dt, start_time)
                            event.append(f'EXDATE;TZID=America/Sao_Paulo:{exdate_str}')
                        except Exception:
                            continue
                event.append('END:VEVENT')
                lines.extend(event)
                counter += 1
                n_events += 1
    lines.append('END:VCALENDAR')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return n_events
