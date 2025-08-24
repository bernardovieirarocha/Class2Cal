import re
from typing import List, Dict, Tuple, Any

DAYS_MAP = {'2': 'MO', '3': 'TU', '4': 'WE', '5': 'TH', '6': 'FR'}
SLOTS_M = {1: ("07:00","07:50"), 2: ("07:50","08:40"), 3: ("08:50","09:40"), 4: ("09:40","10:30"), 5: ("10:40","11:30"), 6: ("11:30","12:20")}
SLOTS_T = {1: ("13:00","13:50"), 2: ("13:50","14:40"), 3: ("14:50","15:40"), 4: ("15:40","16:30"), 5: ("16:40","17:30"), 6: ("17:30","18:20")}
SLOTS_N = {1: ("18:50","19:40"), 2: ("19:40","20:30"), 3: ("20:50","21:40"), 4: ("21:40","22:30")}
TURN_SLOTS = {"M": SLOTS_M, "T": SLOTS_T, "N": SLOTS_N}

CODE_REGEX = re.compile(r'^([2-6]+)([MTN])([1-6]{2})$')

def parse_cefet_codes(codes_str: str) -> List[Dict[str, Any]]:
    codes = re.split(r'[ ,]+', codes_str.strip())
    result = []
    for code in codes:
        m = CODE_REGEX.match(code)
        if not m:
            result.append({'error': f'Código inválido: {code}'})
            continue
        days_str, turn, slots_str = m.groups()
        days = [DAYS_MAP[d] for d in days_str]
        start_slot = int(slots_str[0])
        end_slot = int(slots_str[1])
        if turn == 'N' and end_slot > 4:
            result.append({'error': f'Slot noturno > 4: {code}'})
            continue
        slots_table = TURN_SLOTS[turn]
        start_time = slots_table[start_slot][0]
        end_time = slots_table[end_slot][1]
        result.append({
            'days': days,
            'turn': turn,
            'start_slot': start_slot,
            'end_slot': end_slot,
            'start_time': start_time,
            'end_time': end_time,
            'code': code
        })
    return result
