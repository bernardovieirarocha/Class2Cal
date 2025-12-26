from typing import List, Optional
import datetime
from .models import Course, Semester
from .utils import ics_escape, first_occurrence, format_dt
from .cefet_code import parse_cefet_codes

def generate_ics_content(semester: Semester, courses: List[Course], exdates: Optional[List[datetime.date]] = None) -> str:
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//bernardo//cefet-schedule//PT-BR',
        'CALSCALE:GREGORIAN',
        f'X-WR-CALNAME:{ics_escape(semester.calendar_name)}',
        'X-WR-TIMEZONE:America/Sao_Paulo'
    ]
    
    counter = 1
    
    for course in courses:
        schedule_codes = course.schedule_codes
        code_infos = parse_cefet_codes(schedule_codes)
        
        for info in code_infos:
            if 'error' in info:
                # In a robust system we might want to log this or bubble up warnings
                continue
                
            days = info['days']
            start_time = info['start_time']
            end_time = info['end_time']
            
            for day in days:
                dt = first_occurrence(semester.start_date, day)
                # If first occurrence is after end date, skip (unlikely but possible)
                if dt > semester.end_date:
                    continue
                    
                dtstart = format_dt(dt, start_time)
                dtend = format_dt(dt, end_time)
                until = semester.end_date.strftime('%Y%m%d') + 'T235959Z'
                rrule = f'FREQ=WEEKLY;BYDAY={day};UNTIL={until}'
                
                desc = f"{ics_escape(course.full_name or course.alias)}\\nProfessor: {ics_escape(course.professor)}\\nSala: {ics_escape(course.room)}\\nCódigos: {ics_escape(course.schedule_codes)}"
                
                event = [
                    'BEGIN:VEVENT',
                    f'UID:{datetime.datetime.now().timestamp()}-{counter}@cefet-app',
                    f'SUMMARY:{ics_escape(course.alias)}',
                    f'DESCRIPTION:{desc}',
                    f'LOCATION:{ics_escape(course.room)}',
                    f'DTSTART;TZID=America/Sao_Paulo:{dtstart}',
                    f'DTEND;TZID=America/Sao_Paulo:{dtend}',
                    f'RRULE:{rrule}'
                ]
                
                if exdates:
                    for exd in exdates:
                        exdate_str = format_dt(exd, start_time)
                        event.append(f'EXDATE;TZID=America/Sao_Paulo:{exdate_str}')
                
                event.append('END:VEVENT')
                lines.extend(event)
                counter += 1
                
    lines.append('END:VCALENDAR')
    return '\n'.join(lines)
