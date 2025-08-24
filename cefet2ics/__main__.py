import argparse
from cefet2ics.parser import parse_input, validate_dates
from cefet2ics.ics_writer import write_ics
from cefet2ics.templates import write_templates

def main():
    parser = argparse.ArgumentParser(description="Automatiza a criação de um arquivo iCalendar (.ics) com horários do CEFET.")
    parser.add_argument('--csv', type=str, help='Arquivo CSV de disciplinas')
    parser.add_argument('--json', type=str, help='Arquivo JSON de disciplinas')
    parser.add_argument('--write-templates', action='store_true', help='Gera templates de exemplo CSV/JSON')
    parser.add_argument('--start', type=str, help='Data de início do semestre (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='Data de fim do semestre (YYYY-MM-DD)')
    parser.add_argument('--cal-name', type=str, default='CEFET-Semestre', help='Nome do calendário')
    parser.add_argument('--out', type=str, default='materias.ics', help='Arquivo de saída .ics')
    parser.add_argument('--exdates', type=str, help='Datas a excluir (YYYY-MM-DD,...)')
    args = parser.parse_args()

    if args.write_templates:
        write_templates()
        print('Templates gerados: courses_template.csv, courses_template.json')
        return

    if not (args.csv or args.json):
        print('Erro: informe --csv ou --json.')
        return

    courses, semester_info, errors = parse_input(args)
    start, end = validate_dates(args, semester_info)
    if not start or not end:
        print('Erro nas datas do semestre.')
        return

    n_events = write_ics(courses, start, end, args.cal_name, args.out, args.exdates)
    print(f'Disciplinas processadas: {len(courses)}')
    print(f'Eventos gerados: {n_events}')
    print(f'Arquivo .ics: {args.out}')
    if errors:
        print('Linhas ignoradas por erro:')
        for e in errors:
            print(f'- {e}')

if __name__ == "__main__":
    main()
