import csv
import json
from typing import Any, Dict, List, Tuple
from cefet2ics.cefet_code import parse_cefet_codes

def parse_input(args) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[str]]:
    errors = []
    courses = []
    semester_info = {}
    if args.csv:
        try:
            with open(args.csv, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row.get('alias') or not row.get('schedule_codes'):
                        errors.append(f"Linha inválida: {row}")
                        continue
                    courses.append(row)
        except Exception as e:
            errors.append(str(e))
    elif args.json:
        try:
            with open(args.json, encoding='utf-8') as f:
                data = json.load(f)
                semester_info = data.get('semester', {})
                for course in data.get('courses', []):
                    if not course.get('alias') or not course.get('schedule_codes'):
                        errors.append(f"Curso inválido: {course}")
                        continue
                    courses.append(course)
        except Exception as e:
            errors.append(str(e))
    return courses, semester_info, errors

def validate_dates(args, semester_info):
    import datetime
    start = args.start or semester_info.get('start_date')
    end = args.end or semester_info.get('end_date')
    try:
        start_dt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_dt = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        if start_dt > end_dt:
            return None, None
        return start_dt, end_dt
    except Exception:
        return None, None
