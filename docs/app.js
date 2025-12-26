// --- CONSTANTS & CONFIG ---
const WEEKDAY_MAP = { 'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4 };
const SLOTS_M = { 1: ["07:00", "07:50"], 2: ["07:50", "08:40"], 3: ["08:50", "09:40"], 4: ["09:40", "10:30"], 5: ["10:40", "11:30"], 6: ["11:30", "12:20"] };
const SLOTS_T = { 1: ["13:00", "13:50"], 2: ["13:50", "14:40"], 3: ["14:50", "15:40"], 4: ["15:40", "16:30"], 5: ["16:40", "17:30"], 6: ["17:30", "18:20"] };
const SLOTS_N = { 1: ["18:50", "19:40"], 2: ["19:40", "20:30"], 3: ["20:50", "21:40"], 4: ["21:40", "22:30"] };
const TURN_SLOTS = { "M": SLOTS_M, "T": SLOTS_T, "N": SLOTS_N };
const DAYS_CODE_MAP = { '2': 'MO', '3': 'TU', '4': 'WE', '5': 'TH', '6': 'FR' };
// Regex: Group 1=Days(2-6), Group 2=Turn(MTN), Group 3=Slots(1-6 pair)
const CODE_REGEX = /^([2-6]+)([MTN])([1-6]{2})$/;

// --- STATE ---
let courses = [];
let semester = {
    calendar_name: "Semestre 2025-2",
    start_date: "",
    end_date: ""
};

// --- CORE LOGIC (Ported from Python) ---

/**
 * Parses a CEFET schedule code string (e.g. "24M12 6N34")
 */
function parseCefetCodes(codesStr) {
    const codes = codesStr.trim().split(/[ ,]+/);
    const result = [];

    for (const code of codes) {
        if (!code) continue;
        const m = code.match(CODE_REGEX);
        if (!m) {
            console.warn(`Código inválido ignorado: ${code}`);
            continue;
        }

        const daysStr = m[1];
        const turn = m[2];
        const slotsStr = m[3];

        const days = daysStr.split('').map(d => DAYS_CODE_MAP[d]);
        const startSlot = parseInt(slotsStr[0]);
        const endSlot = parseInt(slotsStr[1]);

        if (turn === 'N' && endSlot > 4) {
            console.warn(`Slot noturno > 4 ignorado: ${code}`);
            continue;
        }

        const slotsTable = TURN_SLOTS[turn];
        if (!slotsTable || !slotsTable[startSlot] || !slotsTable[endSlot]) {
            console.warn(`Slots indefinidos ou fora do range: ${code}`);
            continue;
        }

        const startTime = slotsTable[startSlot][0];
        const endTime = slotsTable[endSlot][1];

        result.push({
            days, turn, startSlot, endSlot, startTime, endTime, code
        });
    }
    return result;
}

/**
 * Helper to get date object from YYYY-MM-DD string
 */
function parseDate(str) {
    // Append T00:00:00 to force local time parsing or avoid TZ issues if needed. 
    // Ideally we treat input as simple dates. 
    // JS Date(str) parses UTC if ISO, but local if YYYY-MM-DD sometimes.
    // Let's use explicit splitting to be safe.
    const [y, m, d] = str.split('-').map(Number);
    return new Date(y, m - 1, d);
}

/**
 * Find first occurrence of weekday >= start_date
 * weekdayStr: 'MO', 'TU', etc.
 */
function firstOccurrence(startDate, weekdayStr) {
    const targetDay = WEEKDAY_MAP[weekdayStr];
    const currentDay = startDate.getDay(); // 0=Sun, 1=Mon...
    // Adjust logic: JS Sunday=0. WEEKDAY_MAP MO=0 is consistent with ics logic? 
    // Wait, Python weekday() Mon=0, Sun=6. JS getDay() Sun=0, Mon=1.
    // Let's Map JS standard:
    // WEEKDAY_MAP for logic calculation:
    // We want target (0=Mon...4=Fri).
    // JS current: 0=Sun, 1=Mon...

    // Map JS current to Python styled (Mon=0...Sun=6)
    const jsToPy = (d) => (d + 6) % 7;
    const currentPy = jsToPy(currentDay);

    const targetPy = targetDay; // 0..4

    let daysAhead = (targetPy - currentPy + 7) % 7;

    const res = new Date(startDate);
    res.setDate(startDate.getDate() + daysAhead);
    return res;
}

/**
 * Format date to iCalendar string: YYYYMMDDTHHMMSS
 */
function formatDt(dateObj, timeStr) {
    const y = dateObj.getFullYear();
    const m = String(dateObj.getMonth() + 1).padStart(2, '0');
    const d = String(dateObj.getDate()).padStart(2, '0');
    const t = timeStr.replace(':', '') + '00';
    return `${y}${m}${d}T${t}`;
}

function icsEscape(str) {
    if (!str) return "";
    return str.replace(/\\/g, '\\\\').replace(/,/g, '\\,').replace(/;/g, '\\;').replace(/\n/g, '\\n');
}

/**
 * Generates the full .ics content string
 */
function generateIcsContent(courses, semester) {
    const lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//bernardo//cefet-schedule//PT-BR',
        'CALSCALE:GREGORIAN',
        `X-WR-CALNAME:${icsEscape(semester.calendar_name)}`,
        'X-WR-TIMEZONE:America/Sao_Paulo'
    ];

    const semStart = parseDate(semester.start_date);
    const semEnd = parseDate(semester.end_date);
    // Set semEnd to end of day? Usually semester end date is inclusive.
    // ISODate for UNTIL needs to be UTC usually.
    // Let's make UNTIL be the end date 23:59:59
    const untilStr = `${semester.end_date.replace(/-/g, '')}T235959Z`;

    let counter = 1;

    courses.forEach(course => {
        const infos = parseCefetCodes(course.schedule_codes);

        infos.forEach(info => {
            info.days.forEach(day => {
                const dt = firstOccurrence(semStart, day);
                if (dt > semEnd) return;

                const dtStart = formatDt(dt, info.startTime);
                const dtEnd = formatDt(dt, info.endTime);

                const desc = `${icsEscape(course.full_name || course.alias)}\\nProfessor: ${icsEscape(course.professor)}\\nSala: ${icsEscape(course.room)}\\nCódigos: ${icsEscape(course.schedule_codes)}`;

                const event = [
                    'BEGIN:VEVENT',
                    `UID:${Date.now()}-${counter}@cefet-app`,
                    `SUMMARY:${icsEscape(course.alias)}`,
                    `DESCRIPTION:${desc}`,
                    `LOCATION:${icsEscape(course.room)}`,
                    `DTSTART;TZID=America/Sao_Paulo:${dtStart}`,
                    `DTEND;TZID=America/Sao_Paulo:${dtEnd}`,
                    `RRULE:FREQ=WEEKLY;BYDAY=${day};UNTIL=${untilStr}`,
                    'END:VEVENT'
                ];
                lines.push(...event);
                counter++;
            });
        });
    });

    lines.push('END:VCALENDAR');
    return lines.join('\r\n'); // CRLF best practice for ICS
}


// --- UI LOGIC ---
const $ = (id) => document.getElementById(id);

function updateUI() {
    const list = $('course-list');
    const empty = $('empty-state');
    const count = $('course-count');

    // Sync inputs
    $('cal-name').value = semester.calendar_name;
    if (semester.start_date) $('start-date').value = semester.start_date;
    if (semester.end_date) $('end-date').value = semester.end_date;

    list.innerHTML = '';

    if (courses.length === 0) {
        list.appendChild(empty);
        empty.style.display = 'flex';
    } else {
        courses.forEach((c, idx) => {
            const el = document.createElement('div');
            el.className = 'bg-slate-50 hover:bg-white border border-slate-200 hover:border-indigo-200 p-4 rounded-xl flex justify-between items-center transition shadow-sm hover:shadow-md slide-in group';
            el.innerHTML = `
                <div>
                    <div class="flex items-center gap-2 mb-1">
                        <span class="font-bold text-slate-800 text-lg">${c.alias}</span>
                        <span class="text-xs font-mono bg-slate-200 text-slate-600 px-2 py-0.5 rounded text-[10px]">${c.schedule_codes}</span>
                    </div>
                    <div class="text-sm text-slate-500">
                        ${c.full_name || ''} 
                        ${c.professor ? `• ${c.professor}` : ''} 
                        ${c.room ? `• ${c.room}` : ''}
                    </div>
                </div>
                <button onclick="removeCourse(${idx})" class="w-8 h-8 rounded-full bg-white border border-slate-200 text-slate-400 hover:text-red-500 hover:border-red-200 flex items-center justify-center transition opacity-0 group-hover:opacity-100">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            `;
            list.appendChild(el);
        });
    }
    count.innerText = `(${courses.length})`;
}

// Input Event Listeners to save state
$('cal-name').addEventListener('input', e => semester.calendar_name = e.target.value);
$('start-date').addEventListener('input', e => semester.start_date = e.target.value);
$('end-date').addEventListener('input', e => semester.end_date = e.target.value);


function addCourse() {
    const alias = $('c-alias').value.trim();
    const scheduleCodes = $('c-codes').value.trim();

    if (!alias || !scheduleCodes) {
        alert("Alias e Códigos são obrigatórios!");
        return;
    }

    const course = {
        alias: alias,
        full_name: $('c-fullname').value.trim(),
        professor: $('c-prof').value.trim(),
        room: $('c-room').value.trim(),
        schedule_codes: scheduleCodes
    };

    courses.push(course);

    // Clear inputs
    $('c-alias').value = '';
    $('c-fullname').value = '';
    $('c-prof').value = '';
    $('c-room').value = '';
    $('c-codes').value = '';
    $('c-alias').focus();

    updateUI();
}

function removeCourse(idx) {
    courses.splice(idx, 1);
    updateUI();
}

function clearCourses() {
    if (confirm('Tem certeza?')) {
        courses = [];
        updateUI();
    }
}

// CSV/JSON Parsing in JS
function parseCSV(text) {
    // Simple CSV parser assuming header row and standard format
    const lines = text.split('\n').map(l => l.trim()).filter(l => l);
    if (lines.length < 2) return [];
    const headers = lines[0].split(',').map(h => h.trim());

    // Map header names to keys
    const newCourses = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(','); // Naive split, careful with commas in quotes
        if (values.length !== headers.length) continue;

        let c = {};
        headers.forEach((h, idx) => {
            c[h] = values[idx];
        });

        if (c.alias && c.schedule_codes) newCourses.push(c);
    }
    return newCourses;
}

function handleFileUpload(input) {
    const file = input.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const text = e.target.result;
        try {
            if (file.name.endsWith('.json')) {
                const data = JSON.parse(text);
                courses = data.courses || [];
                if (data.semester) semester = { ...semester, ...data.semester };
            } else {
                const newC = parseCSV(text);
                courses = [...courses, ...newC];
            }
            updateUI();
            alert('Arquivo carregado com sucesso!');
        } catch (err) {
            alert('Erro ao processar arquivo: ' + err.message);
        }
    };
    reader.readAsText(file);
    input.value = '';
}

function generateCalendar() {
    if (!semester.start_date || !semester.end_date || courses.length === 0) {
        alert("Preencha as datas do semestre e adicione pelo menos uma disciplina.");
        return;
    }

    try {
        const icsContent = generateIcsContent(courses, semester);

        // Download
        const blob = new Blob([icsContent], { type: 'text/calendar' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${semester.calendar_name.replace(/\s+/g, '_')}.ics`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();

    } catch (e) {
        console.error(e);
        alert('Erro ao gerar calendário: ' + e.message);
    }
}

// Initial
updateUI();
